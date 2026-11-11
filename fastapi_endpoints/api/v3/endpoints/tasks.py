from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from core.config import get_db
from core.security import AuthenticatedUser, get_current_user, require_teacher
from db.database import Task, User
from models.users_v3 import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskCreateResponse,
    TaskListResponse,
    StudentTaskListResponse,
)

router_task = APIRouter(
    tags=["Tasks"]
)


@router_task.post(
    "/",
    response_model=TaskCreateResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_teacher)],
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    assignee = db.query(User).filter(User.id == task.user_id).first()
    if assignee is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if assignee.role != "student":
        raise HTTPException(status_code=400, detail="Tasks can only be assigned to students")

    new_task = Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {
        "message": "Task created and assigned successfully",
        "data": new_task
    }


@router_task.get("/", response_model=TaskListResponse)
def get_tasks(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    status: str | None = Query(
        default=None,
        pattern="^(pending|in_progress|done)$",
    ),
    user_id: int | None = Query(default=None, ge=1),
    assigned_user: int | None = Query(default=None, ge=1),
    search: str | None = Query(default=None),
    title: str | None = Query(default=None),
    current: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_id is None and assigned_user is not None:
        user_id = assigned_user

    if title is not None and search is None:
        search = title
    elif title is not None and search is not None:
        search = search or title

    query = db.query(Task)
    if current.user.role == "student":
        query = query.filter(Task.user_id == current.user.id)
    if status:
        query = query.filter(Task.status == status)
    if user_id is not None:
        query = query.filter(Task.user_id == user_id)
    if search and search.strip():
        query = query.filter(Task.title.ilike(f"%{search.strip()}%"))

    total_tasks = query.count()
    total_pages = (total_tasks + limit - 1) // limit if total_tasks else 1
    tasks = query.order_by(Task.id).offset((page - 1) * limit).limit(limit).all()

    return {
        "message": "Tasks fetched successfully",
        "page": page,
        "limit": limit,
        "total_tasks": total_tasks,
        "total_pages": total_pages,
        "data": tasks,
    }


@router_task.get("/progress")
def get_progress(
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(require_teacher),
):
    status_counts = {
        row.status: row.total
        for row in db.query(Task.status, func.count(Task.id).label("total"))
        .group_by(Task.status)
        .all()
    }
    students = db.query(User).filter(User.role == "student").order_by(User.id).all()
    student_counts: dict[int, dict[str, int]] = {}
    for row in (
        db.query(Task.user_id, Task.status, func.count(Task.id).label("total"))
        .group_by(Task.user_id, Task.status)
        .all()
    ):
        student_counts.setdefault(row.user_id, {})[row.status] = row.total

    return {
        "total_tasks": sum(status_counts.values()),
        "by_status": {
            task_status: status_counts.get(task_status, 0)
            for task_status in ("pending", "in_progress", "done")
        },
        "students": [
            {
                "user_id": student.id,
                "name": student.name,
                "total_tasks": sum(student_counts.get(student.id, {}).values()),
                "by_status": {
                    task_status: student_counts.get(student.id, {}).get(task_status, 0)
                    for task_status in ("pending", "in_progress", "done")
                },
            }
            for student in students
        ],
    }


@router_task.get("/students", response_model=StudentTaskListResponse)
def get_student_tasks(
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(require_teacher),
):
    rows = (
        db.query(User, Task)
        .outerjoin(Task, Task.user_id == User.id)
        .filter(User.role == "student")
        .order_by(User.id, Task.id)
        .all()
    )
    students: dict[int, dict] = {}
    for student, task in rows:
        student_data = students.setdefault(
            student.id,
            {"user_id": student.id, "name": student.name, "total_tasks": 0, "tasks": []},
        )
        if task is not None:
            student_data["tasks"].append(task)
            student_data["total_tasks"] += 1

    return {"message": "Student tasks fetched successfully", "data": list(students.values())}


# GET SINGLE TASK
@router_task.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Task).filter(Task.id == task_id)
    if current.user.role == "student":
        query = query.filter(Task.user_id == current.user.id)
    task = query.first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router_task.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Task).filter(Task.id == task_id)
    if current.user.role == "student":
        query = query.filter(Task.user_id == current.user.id)
    task = query.first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_data.model_dump(exclude_unset=True)
    if current.user.role == "student":
        forbidden_fields = set(update_data) - {"status", "work_notes"}
        if forbidden_fields:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students may only update task status and work notes",
            )
        if update_data.get("status") == "pending":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students may only set task status to in_progress or done",
            )
    elif update_data.get("status") not in (None, "pending"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teachers may only set task status to pending",
        )
    if "user_id" in update_data:
        assignee = db.query(User).filter(User.id == update_data["user_id"]).first()
        if assignee is None:
            raise HTTPException(status_code=404, detail="Student not found")
        if assignee.role != "student":
            raise HTTPException(status_code=400, detail="Tasks can only be assigned to students")
    for key, value in update_data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


@router_task.delete("/{task_id}", dependencies=[Depends(require_teacher)])
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {
        "message": "Task deleted successfully"
    }
