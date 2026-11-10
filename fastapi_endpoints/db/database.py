from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.config import Base


# USERS MODEL
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    status = Column(String(20), default="active")
    password_hash = Column(String(255), nullable=True)
    role = Column(
        String(20),
        nullable=False,
        default="student",
        server_default=text("'student'")
    )
    created_at = Column(DateTime, server_default=func.now())

    tasks = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    auth_sessions = relationship(
        "AuthSession",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


# TASKS MODEL
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="pending", nullable=False)
    work_notes = Column(Text, nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="tasks")


class AuthSession(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    refresh_token_hash = Column(String(64), nullable=False, unique=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user = relationship("User", back_populates="auth_sessions")