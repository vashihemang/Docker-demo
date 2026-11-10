from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class Usercreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    phone: str | None = Field(default=None, max_length=20)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    phone: str | None = None
    role: Literal["teacher", "student"]
    created_at: datetime


class UserCreateResponse(BaseModel):
    message: str
    data: UserResponse


class UserListResponse(BaseModel):
    message: str
    total_users: int = Field(..., ge=0)
    data: list[UserResponse]


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)


class UserDetailResponse(BaseModel):
    message: str
    data: UserResponse


class UserDeleteResponse(BaseModel):
    message: str


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., min_length=2, max_length=200)
    description: str | None = Field(default=None, max_length=10000)
    status: Literal["pending"] = "pending"
    user_id: int = Field(..., gt=0)

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Title must contain at least 2 non-whitespace characters")
        return value


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = Field(default=None, max_length=10000)
    status: Literal["pending", "in_progress", "done"] | None = None
    user_id: int | None = Field(default=None, gt=0)
    work_notes: str | None = Field(default=None, max_length=20000)

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Title must contain at least 2 non-whitespace characters")
        return value

    @model_validator(mode="after")
    def validate_changes(self) -> "TaskUpdate":
        if not self.model_fields_set:
            raise ValueError("At least one task field must be provided")
        if "status" in self.model_fields_set and self.status is None:
            raise ValueError("Status cannot be null")
        if "user_id" in self.model_fields_set and self.user_id is None:
            raise ValueError("Assignee cannot be null")
        if "title" in self.model_fields_set and self.title is None:
            raise ValueError("Title cannot be null")
        return self


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: Literal["pending", "in_progress", "done"]
    work_notes: str | None
    user_id: int
    created_at: datetime


class TaskCreateResponse(BaseModel):
    message: str
    data: TaskResponse


class TaskListResponse(BaseModel):
    message: str
    total_tasks: int
    data: list[TaskResponse]


class StudentTasksResponse(BaseModel):
    user_id: int
    name: str
    total_tasks: int
    tasks: list[TaskResponse]


class StudentTaskListResponse(BaseModel):
    message: str
    data: list[StudentTasksResponse]


class UserWithTasksResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    phone: str | None
    status: str
    role: Literal["teacher", "student"]
    created_at: datetime
    tasks: list[TaskResponse]
