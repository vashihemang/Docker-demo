from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.config import get_db
from db.database import User 
from models.users_v3 import (
    Usercreate,
    UserUpdate,
    UserCreateResponse,
    UserListResponse,
    UserDetailResponse,
    UserWithTasksResponse
)

router_v3 = APIRouter(
    tags=["Users"]
)


# CREATE USER
@router_v3.post(
    "/users",
    response_model=UserCreateResponse,
    status_code=201
)
def create_user(
    user: Usercreate,
    db: Session = Depends(get_db)
):
    try:
        # Debugging
        print("Incoming Email:", repr(user.email))

        # Check duplicate email
        existing_user = db.query(User).filter(
            User.email == user.email
        ).first()

        print("Existing User:", existing_user)

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

        # Create new user
        new_user = User(
            name=user.name,
            age=user.age,
            email=user.email,
            phone=user.phone,
            status=user.is_active
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User created successfully",
            "data": new_user
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise

# GET ALL USERS
@router_v3.get("/all_users", response_model=UserListResponse)
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return {
        "message": "Users fetched successfully",
        "total_users": len(users),
        "data": users
    }


# GET SINGLE USER
@router_v3.get("/user/{user_id}", response_model=UserDetailResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User details fetched successfully",
        "data": user
    }


# GET USER WITH ALL TASKS
@router_v3.get("/{user_id}/tasks", response_model=UserWithTasksResponse)
def get_user_with_tasks(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# UPDATE USER
@router_v3.put("/{user_id}", response_model=UserDetailResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    update_data = user_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    if "email" in update_data:
        existing = db.query(User).filter(
            User.email == update_data["email"],
            User.id != user_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "data": user
    }


# DELETE USER
@router_v3.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }