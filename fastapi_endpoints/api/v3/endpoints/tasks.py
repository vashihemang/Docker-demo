from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.config import get_db
from db.database import Task,User
from models.users_v3 import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskCreateResponse,
    TaskListResponse
)

router_task = APIRouter(
    tags=["Tasks"]
)


# CREATE TASK / ASSIGN TASK TO USER
@router_task.post("/", response_model=TaskCreateResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):

    # Check whether user exists
    user = db.query(User).filter(
        User.id == task.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found. Cannot assign task."
        )

    new_task = Task(**task.model_dump())

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task created and assigned successfully",
        "data": new_task
    }


# GET ALL TASKS + FILTER BY STATUS
@router_task.get("/", response_model=TaskListResponse)
def get_tasks(
    status: str | None = Query(
        default=None,
        pattern="^(pending|in_progress|done)$"
    ),
    db: Session = Depends(get_db)
):

    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)

    tasks = query.all()

    return {
        "message": "Tasks fetched successfully",
        "total_tasks": len(tasks),
        "data": tasks
    }


# GET SINGLE TASK
@router_task.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# UPDATE TASK
@router_task.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = task_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    # Check user before reassigning task
    if "user_id" in update_data:

        user = db.query(User).filter(
            User.id == update_data["user_id"]
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# DELETE TASK
@router_task.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }