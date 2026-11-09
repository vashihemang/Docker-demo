from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import inspect, text

from core.config import Base, engine


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


def initialize_database() -> None:
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    with engine.begin() as connection:
        if "users" in existing_tables:
            user_columns = {
                column["name"] for column in inspect(connection).get_columns("users")
            }
            if "password_hash" not in user_columns:
                connection.execute(
                    text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)")
                )
            if "role" not in user_columns:
                connection.execute(
                    text(
                        "ALTER TABLE users ADD COLUMN role VARCHAR(20) "
                        "NOT NULL DEFAULT 'student'"
                    )
                )
        if "tasks" in existing_tables:
            task_columns = {
                column["name"] for column in inspect(connection).get_columns("tasks")
            }
            if "work_notes" not in task_columns:
                connection.execute(text("ALTER TABLE tasks ADD COLUMN work_notes TEXT"))

    Base.metadata.create_all(bind=engine)