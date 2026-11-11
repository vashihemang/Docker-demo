
from fastapi import APIRouter, Body, Depends, HTTPException
import asyncio

from core.security import require_teacher

router = APIRouter(
    tags=["Users"],
    dependencies=[Depends(require_teacher)],
)

# Temporary in-memory database
users = []
user_id_counter = 1


# 1. Create User (POST)
@router.post("/users")
async def create_user(
    user: dict = Body(
        ...,
        examples={
            "default": {
                "summary": "Example user",
                "value": {
                    "name": "Rahul Sharma",
                    "email": "rahul@gmail.com",
                    "phone": "9876543210",
                    "status": "active",
                },
            }
        },
    )
):
    global user_id_counter

    # Async operation
    await asyncio.sleep(0)

    # Required field validation
    if not user.get("name") or not user.get("email"):
        raise HTTPException(
            status_code=400,
            detail="Name and email are required"
        )

    # Check duplicate email
    for existing_user in users:
        if existing_user["email"] == user["email"]:
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

    new_user = {
        "id": user_id_counter,
        "name": user.get("name"),
        "email": user.get("email"),
        "phone": user.get("phone"),
        "status": user.get("status", "active")
    }

    users.append(new_user)

    user_id_counter += 1

    return {
        "message": "User created successfully",
        "data": new_user
    }


# 2. Get All Users (GET)
@router.get("/all_users")
async def get_users():

    await asyncio.sleep(0)

    return {
        "message": "Users fetched successfully",
        "total_users": len(users),
        "data": users
    }

# 3. Get User By ID (GET)
@router.get("/fetch/user/{user_id}")
async def get_user(user_id: int):

    await asyncio.sleep(0)

    for user in users:
        if user["id"] == user_id:

            return {
                "message": "User fetched successfully",
                "data": user
            }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )

# 3. Update User (PUT)
@router.put("/user/{user_id}")
async def update_user(
    user_id: int,
    user_data: dict = Body(
        ...,
        examples={
            "default": {
                "summary": "Example user",
                "value": {
                    "name": "Rahul Sharma",
                    "email": "rahul@gmail.com",
                    "phone": "9876543210",
                    "status": "active",
                },
            }
        },
    )
):

    await asyncio.sleep(0)

    for user in users:
        if user["id"] == user_id:

            user["name"] = user_data.get("name", user["name"])
            user["email"] = user_data.get("email", user["email"])
            user["phone"] = user_data.get("phone", user["phone"])
            user["status"] = user_data.get("status", user["status"])

            return {
                "message": "User updated successfully",
                "data": user
            }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


# 4. Delete User (DELETE)
@router.delete("/user/{user_id}")
async def delete_user(user_id: int):

    await asyncio.sleep(0)

    for user in users:
        if user["id"] == user_id:

            users.remove(user)

            return {
                "message": "User deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )
