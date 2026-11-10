from datetime import datetime, timezone
import hmac
import os

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.config import get_db
from core.security import (
    AuthenticatedUser,
    create_session_tokens,
    get_current_user,
    hash_password,
    rotate_refresh_token,
    verify_password,
)
from db.database import AuthSession, User
from models.auth import (
    LoginRequest,
    MessageResponse,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserProfile,
)

router_auth = APIRouter(tags=["Authentication"])


def _register_user(payload: RegisterRequest, role: str, db: Session) -> User:
    email = str(payload.email).lower()
    existing_user = (
        db.query(User)
        .filter(func.lower(User.email) == email)
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        name=payload.name,
        email=email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
        role=role,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered") from exc
    db.refresh(user)
    return user


def _authenticate(
    payload: LoginRequest,
    db: Session,
    required_role: str | None = None,
) -> TokenResponse:
    email = str(payload.email).lower()
    user = db.query(User).filter(func.lower(User.email) == email).first()
    if (
        user is None
        or user.status != "active"
        or (required_role is not None and user.role != required_role)
        or not verify_password(payload.password, user.password_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_session_tokens(db, user)


@router_auth.post(
    "/register",
    response_model=UserProfile,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> User:
    return _register_user(payload, "student", db)


@router_auth.post(
    "/teacher/register",
    response_model=UserProfile,
    status_code=status.HTTP_201_CREATED,
)
def register_teacher(
    payload: RegisterRequest,
    registration_key: str = Header(alias="X-Teacher-Registration-Key"),
    db: Session = Depends(get_db),
) -> User:
    configured_key = os.getenv("TEACHER_REGISTRATION_KEY", "")
    if len(configured_key.encode("utf-8")) < 32:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Teacher registration is not configured; set TEACHER_REGISTRATION_KEY",
        )
    if not hmac.compare_digest(registration_key, configured_key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid teacher registration key",
        )
    return _register_user(payload, "teacher", db)


@router_auth.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return _authenticate(payload, db)


@router_auth.post("/student/login", response_model=TokenResponse)
def login_student(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    return _authenticate(payload, db, required_role="student")


@router_auth.post("/teacher/login", response_model=TokenResponse)
def login_teacher(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    return _authenticate(payload, db, required_role="teacher")


@router_auth.post("/refresh", response_model=TokenResponse)
def refresh(
    payload: RefreshRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    return rotate_refresh_token(db, payload.refresh_token)


@router_auth.post("/logout", response_model=MessageResponse)
def logout(
    current: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageResponse:
    session = (
        db.query(AuthSession)
        .filter(
            AuthSession.id == current.session_id,
            AuthSession.user_id == current.user.id,
            AuthSession.revoked_at.is_(None),
        )
        .first()
    )
    if session is not None:
        session.revoked_at = datetime.now(timezone.utc)
        db.commit()
    return MessageResponse(message="Session logged out")


@router_auth.get("/me", response_model=UserProfile)
def me(current: AuthenticatedUser = Depends(get_current_user)) -> User:
    return current.user
