from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi.testclient import TestClient

from core.config import SessionLocal, engine
from core.security import hash_password
from db.database import AuthSession, Base, User
from main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        with SessionLocal.begin() as db:
            db.add(
                User(
                    name="Test Teacher",
                    email="teacher@example.com",
                    password_hash=hash_password("teacher-pass-123"),
                    role="teacher",
                    status="active",
                )
            )
        yield test_client
        Base.metadata.drop_all(engine)


def login(client: TestClient, email: str, password: str) -> dict[str, str]:
    response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response.json()


def bearer(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_teacher_student_task_permissions_and_validation(client: TestClient):
    assert client.get("/tasks/").status_code == 401
    assert client.get("/api/v3/all_users").status_code == 401

    invalid_registration = client.post(
        "/auth/register",
        json={"name": "Student", "email": "not-an-email", "password": "short"},
    )
    assert invalid_registration.status_code == 422

    registration = client.post(
        "/auth/register",
        json={
            "name": "Test Student",
            "email": "student@example.com",
            "password": "student-pass-123",
        },
    )
    assert registration.status_code == 201
    assert registration.json()["role"] == "student"
    assert "password_hash" not in registration.json()
    student_id = registration.json()["id"]
    assert client.post(
        "/auth/register",
        json={
            "name": "Duplicate Student",
            "email": "STUDENT@example.com",
            "password": "student-pass-123",
        },
    ).status_code == 409
    assert client.post(
        "/auth/login",
        json={"email": "student@example.com", "password": "wrong-password"},
    ).status_code == 401

    student_login = client.post(
        "/auth/student/login",
        json={"email": "student@example.com", "password": "student-pass-123"},
    )
    assert student_login.status_code == 200
    assert "access_token" in student_login.json()
    assert client.post(
        "/auth/student/login",
        json={"email": "teacher@example.com", "password": "teacher-pass-123"},
    ).status_code == 401

    teacher_tokens = login(client, "teacher@example.com", "teacher-pass-123")
    student_tokens = login(client, "student@example.com", "student-pass-123")
    teacher_headers = bearer(teacher_tokens["access_token"])
    student_headers = bearer(student_tokens["access_token"])

    created = client.post(
        "/tasks/",
        headers=teacher_headers,
        json={"title": "Finish the assignment", "user_id": student_id},
    )
    assert created.status_code == 201
    task_id = created.json()["data"]["id"]
    assert created.json()["data"]["status"] == "pending"

    student_tasks = client.get("/tasks/", headers=student_headers)
    assert student_tasks.status_code == 200
    assert [task["id"] for task in student_tasks.json()["data"]] == [task_id]
    assert client.get(
        f"/tasks/{task_id}",
        headers=student_headers,
    ).status_code == 200

    updated = client.put(
        f"/tasks/{task_id}",
        headers=student_headers,
        json={"status": "in_progress", "work_notes": "Started the work"},
    )
    assert updated.status_code == 200
    assert updated.json()["work_notes"] == "Started the work"

    assert client.put(
        f"/tasks/{task_id}",
        headers=student_headers,
        json={"user_id": student_id},
    ).status_code == 403
    assert client.put(
        f"/tasks/{task_id}",
        headers=student_headers,
        json={"title": "Changed by student"},
    ).status_code == 403
    assert client.delete(
        f"/tasks/{task_id}",
        headers=student_headers,
    ).status_code == 403
    assert client.get("/tasks/progress", headers=student_headers).status_code == 403
    assert client.get("/tasks/students", headers=student_headers).status_code == 403
    assert client.get("/api/v3/all_users", headers=student_headers).status_code == 403
    assert client.get("/api/v3/all_users", headers=teacher_headers).status_code == 200
    assert client.get("/tasks/", headers=teacher_headers).json()["total_tasks"] == 1
    student_task_overview = client.get("/tasks/students", headers=teacher_headers)
    assert student_task_overview.status_code == 200
    first_student_data = student_task_overview.json()["data"][0]
    assert first_student_data["user_id"] == student_id
    assert first_student_data["name"] == "Test Student"
    assert first_student_data["total_tasks"] == 1
    assert first_student_data["tasks"][0]["id"] == task_id
    assert first_student_data["tasks"][0]["status"] == "in_progress"

    assert client.post(
        "/tasks/",
        headers=student_headers,
        json={"title": "Unauthorized task", "user_id": student_id},
    ).status_code == 403
    assert client.post(
        "/tasks/",
        headers=teacher_headers,
        json={"title": "Bad status", "status": "finished", "user_id": student_id},
    ).status_code == 422
    assert client.post(
        "/tasks/",
        headers=teacher_headers,
        json={"title": "Premature status", "status": "in_progress", "user_id": student_id},
    ).status_code == 422
    assert client.post(
        "/tasks/",
        headers=teacher_headers,
        json={"title": "Missing student", "user_id": 99999},
    ).status_code == 404
    assert client.get("/tasks/99999", headers=teacher_headers).status_code == 404
    assert client.get("/tasks/progress", headers=teacher_headers).json()["by_status"] == {
        "pending": 0,
        "in_progress": 1,
        "done": 0,
    }
    assert client.get(
        "/api/v3/user/99999",
        headers=teacher_headers,
    ).status_code == 404

    second_registration = client.post(
        "/auth/register",
        json={
            "name": "Second Student",
            "email": "second@example.com",
            "password": "student-pass-456",
        },
    )
    second_student_id = second_registration.json()["id"]
    second_task = client.post(
        "/tasks/",
        headers=teacher_headers,
        json={"title": "Private task", "user_id": second_student_id},
    ).json()["data"]
    all_student_tasks = client.get("/tasks/students", headers=teacher_headers).json()["data"]
    assert [student["name"] for student in all_student_tasks] == [
        "Test Student",
        "Second Student",
    ]
    assert [task["title"] for task in all_student_tasks[1]["tasks"]] == ["Private task"]
    assert client.put(
        f"/tasks/{second_task['id']}",
        headers=teacher_headers,
        json={"status": "done"},
    ).status_code == 403
    assert client.put(
        f"/tasks/{second_task['id']}",
        headers=student_headers,
        json={"status": "pending"},
    ).status_code == 404
    second_student_headers = bearer(
        login(client, "second@example.com", "student-pass-456")["access_token"]
    )
    assert client.put(
        f"/tasks/{second_task['id']}",
        headers=second_student_headers,
        json={"status": "done"},
    ).status_code == 200
    assert client.get(
        f"/tasks/{second_task['id']}",
        headers=student_headers,
    ).status_code == 404
    assert client.put(
        f"/tasks/{second_task['id']}",
        headers=student_headers,
        json={"status": "done"},
    ).status_code == 404

    teacher_update = client.put(
        f"/tasks/{task_id}",
        headers=teacher_headers,
        json={"title": "Teacher-reviewed assignment", "user_id": second_student_id},
    )
    assert teacher_update.status_code == 200
    second_student_tokens = login(client, "second@example.com", "student-pass-456")
    assert client.get(
        f"/tasks/{task_id}",
        headers=bearer(second_student_tokens["access_token"]),
    ).json()["title"] == "Teacher-reviewed assignment"

    assert client.put(
        f"/tasks/{second_task['id']}",
        headers=teacher_headers,
        json={"title": "Teacher updated task"},
    ).status_code == 200
    assert client.delete(
        f"/tasks/{second_task['id']}",
        headers=teacher_headers,
    ).status_code == 200


def test_teacher_registration_and_login_require_teacher_credentials(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
):
    registration_key = "test-teacher-registration-key-that-is-long-enough"
    monkeypatch.setenv("TEACHER_REGISTRATION_KEY", registration_key)
    teacher_payload = {
        "name": "New Teacher",
        "email": "new-teacher@example.com",
        "password": "teacher-pass-456",
    }

    assert client.post(
        "/auth/teacher/register",
        json=teacher_payload,
        headers={"X-Teacher-Registration-Key": "wrong-key"},
    ).status_code == 403

    registration = client.post(
        "/auth/teacher/register",
        json=teacher_payload,
        headers={"X-Teacher-Registration-Key": registration_key},
    )
    assert registration.status_code == 201
    assert registration.json()["role"] == "teacher"
    assert "password_hash" not in registration.json()

    teacher_login = client.post(
        "/auth/teacher/login",
        json={
            "email": teacher_payload["email"],
            "password": teacher_payload["password"],
        },
    )
    assert teacher_login.status_code == 200
    assert "access_token" in teacher_login.json()

    student_registration = client.post(
        "/auth/register",
        json={
            "name": "New Student",
            "email": "new-student@example.com",
            "password": "student-pass-456",
        },
    )
    assert student_registration.status_code == 201
    assert client.post(
        "/auth/teacher/login",
        json={
            "email": "new-student@example.com",
            "password": "student-pass-456",
        },
    ).status_code == 401


def test_teacher_registration_requires_configuration(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.delenv("TEACHER_REGISTRATION_KEY", raising=False)
    response = client.post(
        "/auth/teacher/register",
        json={
            "name": "New Teacher",
            "email": "unconfigured-teacher@example.com",
            "password": "teacher-pass-456",
        },
        headers={"X-Teacher-Registration-Key": "any-key"},
    )
    assert response.status_code == 503


def test_refresh_rotation_and_logout_revoke_sessions(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "name": "Test Student",
            "email": "student@example.com",
            "password": "student-pass-123",
        },
    )
    tokens = login(client, "student@example.com", "student-pass-123")

    with SessionLocal() as db:
        session = db.query(AuthSession).one()
        assert session.refresh_token_hash != tokens["refresh_token"]
        assert len(session.refresh_token_hash) == 64

    refreshed = client.post(
        "/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert refreshed.status_code == 200
    new_tokens = refreshed.json()
    assert client.post(
        "/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    ).status_code == 401
    assert client.get("/auth/me", headers=bearer(new_tokens["access_token"])).status_code == 200

    logout = client.post("/auth/logout", headers=bearer(new_tokens["access_token"]))
    assert logout.status_code == 200
    assert client.get("/auth/me", headers=bearer(new_tokens["access_token"])).status_code == 401
    assert client.post(
        "/auth/refresh",
        json={"refresh_token": new_tokens["refresh_token"]},
    ).status_code == 401


def test_expired_access_and_refresh_sessions_are_rejected(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "name": "Test Student",
            "email": "student@example.com",
            "password": "student-pass-123",
        },
    )
    tokens = login(client, "student@example.com", "student-pass-123")
    claims = jwt.decode(
        tokens["access_token"],
        options={"verify_signature": False, "verify_exp": False},
        algorithms=["HS256"],
    )
    claims["exp"] = datetime.now(timezone.utc) - timedelta(seconds=1)
    expired_access = jwt.encode(
        claims,
        "test-only-secret-key-with-at-least-32-bytes",
        algorithm="HS256",
    )
    assert client.get("/auth/me", headers=bearer(expired_access)).status_code == 401

    with SessionLocal.begin() as db:
        session = db.query(AuthSession).one()
        session.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    assert client.get(
        "/auth/me",
        headers=bearer(tokens["access_token"]),
    ).status_code == 401
    assert client.post(
        "/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    ).status_code == 401
