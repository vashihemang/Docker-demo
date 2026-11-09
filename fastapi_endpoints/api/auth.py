from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
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


@router_auth.post(
    "/register",
    response_model=UserProfile,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> User:
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
        role="student",
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered") from exc
    db.refresh(user)
    return user


@router_auth.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    email = str(payload.email).lower()
    user = db.query(User).filter(func.lower(User.email) == email).first()
    if (
        user is None
        or user.status != "active"
        or not verify_password(payload.password, user.password_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_session_tokens(db, user)


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
