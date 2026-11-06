from pydantic import BaseModel , Field ,EmailStr,  ConfigDict
from typing import Optional
import datetime 
# Create data validation and error message : - 

# Create a users 
class Usercreate (BaseModel) : 
    name: str = Field(...,description="Full name of the user",examples=["Rahul Sharma"])
    email: EmailStr = Field(...,description="Registered email address",examples=["rahul@gmail.com"])
    phone: str | None = Field(default=None,description="Registered contact number",examples=["9876543210"])
    
    

# Create User Response
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(...,description="Unique ID assigned to the user",examples=[1])
    name: str = Field(...,description="Full name of the user",examples=["Rahul Sharma"])
    email: EmailStr = Field(...,description="Registered email address",examples=["rahul@gmail.com"])
    phone: str | None = Field(default=None,description="Registered contact number",examples=["9876543210"])
    


# Show created user response
class UserCreateResponse(BaseModel):
    message: str = Field(description="Success message after creating a user",examples=["User created successfully"])
    data: UserResponse = Field(description="Details of the newly created user")

# show all users data

class UserListResponse(BaseModel):

    message: str = Field(...,description="Success message after fetching all users",examples=["Users fetched successfully"])
    total_users: int = Field(...,ge=0,description="Total number of registered users",examples=[5])
    data: list[UserResponse] = Field(...,description="List of all registered users")




# Update User Schema
class UserUpdate(BaseModel):
    name: str | None = Field(default=None,min_length=2,max_length=50,description="Updated full name of the user",examples=["Rahul Sharma"])
   
    email: EmailStr | None = Field(default=None,description="Updated valid email address",examples=["rahul@gmail.com"])
    phone: str | None = Field(default=None,min_length=10,max_length=15,description="Updated contact number",examples=["9876543210"])






# Fetch Single User Response
class UserDetailResponse(BaseModel):
    message: str = Field(
        description="Response message after fetching or updating a user",
        examples=["User details fetched successfully"]
    )
    data: UserResponse

# Delete User Response
class UserDeleteResponse(BaseModel):

    message: str = Field(
        description="Success message after deleting a user",
        examples=["User deleted successfully"]
    )




class TaskCreate(BaseModel):

    title: str = Field(
        ...,
        min_length=2,
        max_length=200,
        examples=["Complete FastAPI Project"],
        description="Task title"
    )

    description: Optional[str] = Field(
        default=None,
        examples=["Develop CRUD APIs using FastAPI and PostgreSQL"],
        description="Task description"
    )

    status: str = Field(
        default="pending",
        pattern="^(pending|in_progress|done)$",
        examples=["pending"],
        description="Task status: pending, in_progress, done"
    )

    user_id: int = Field(
        ...,
        gt=0,
        examples=[1],
        description="ID of the user assigned to this task"
    )


class TaskUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=200,
        examples=["Updated FastAPI Project"],
        description="Updated task title"
    )

    description: Optional[str] = Field(
        default=None,
        examples=["Updated task description"],
        description="Updated task description"
    )

    status: Optional[str] = Field(
        default=None,
        pattern="^(pending|in_progress|done)$",
        examples=["in_progress"],
        description="Task status"
    )

    user_id: Optional[int] = Field(
        default=None,
        gt=0,
        examples=[2],
        description="New assigned user ID"
    )


class TaskResponse(BaseModel):

    id: int = Field(
        examples=[1]
    )

    title: str = Field(
        examples=["Complete FastAPI Project"]
    )

    description: Optional[str] = Field(
        examples=["Develop CRUD APIs"]
    )

    status: str = Field(
        examples=["pending"]
    )

    user_id: int = Field(
        examples=[1]
    )

    created_at: datetime.datetime = Field(
        examples=["2026-11-06T10:30:00Z"]
    )

    model_config = ConfigDict(from_attributes=True)


class TaskCreateResponse(BaseModel):

    message: str = Field(
        examples=["Task created successfully"]
    )

    data: TaskResponse


class TaskListResponse(BaseModel):

    message: str = Field(
        examples=["Tasks fetched successfully"]
    )

    total_tasks: int = Field(
        examples=[2]
    )

    data: list[TaskResponse]


# =========================
# USER WITH TASKS
# =========================

class UserWithTasksResponse(BaseModel):

    id: int = Field(
        examples=[1]
    )

    name: str = Field(
        examples=["Rahul Patel"]
    )

    email: EmailStr = Field(
        examples=["rahul@gmail.com"]
    )

    phone: Optional[str] = Field(
        examples=["9876543210"]
    )

    status: str = Field(
        examples=["active"]
    )

    created_at: datetime.datetime = Field(
        examples=["2026-11-06T10:00:00Z"]
    )

    tasks: list[TaskResponse]

    model_config = ConfigDict(from_attributes=True)
