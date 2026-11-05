from fastapi import APIrouter_v2, Body, HTTPException , status
from models.user import Usercreate,UserCreateResponse,UserListResponse , UserUpdate , UserDetailResponse ,UserDeleteResponse
import asyncio

router_v2 = APIrouter_v2(
    prefix="/api/v2",
    tags=["Users"]
)

# Temporary in-memory database
users = []
user_id_counter = 1


# 1. Create User (POST)
@router_v2.post("/users",response_model=UserCreateResponse,status_code=status.HTTP_201_CREATED)
async def create_user(user: Usercreate):

    global user_id_counter

    await asyncio.sleep(0)


    # Create New User
    new_user = {
        "id": user_id_counter,
        "name": user.name,
        "age": user.age,
        "email": user.email,
        "phone": user.phone,
        "is_active": user.is_active
    }

    users.append(new_user)

    user_id_counter += 1

    return {
        "message": "User created successfully",
        "data": new_user
    }


# 2. Get All Users (GET)
@router_v2.get("/all_users",response_model=UserListResponse,status_code=status.HTTP_200_OK)
async def get_users():

    await asyncio.sleep(0)

    return {
        "message": "Users fetched successfully",
        "total_users": len(users),
        "data": users
    }

# 3. Get User By ID (GET)
@router_v2.get(
    "/fetch/user/{user_id}",
    response_model=UserDetailResponse,
    status_code=status.HTTP_200_OK
)
async def get_user(user_id: int):

    await asyncio.sleep(0)

    for user in users:

        if user["id"] == user_id:

            return {
                "message": "User fetched successfully",
                "data": user
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )



# 3. Update User (PUT)
@router_v2.put(
    "/user/{user_id}",
    response_model=UserDetailResponse,
    status_code=status.HTTP_200_OK
)
async def update_user(
    user_id: int,
    user_data: UserUpdate
):

    await asyncio.sleep(0)

    # Find User
    for user in users:

        if user["id"] == user_id:

            # Convert Pydantic model into dictionary
            update_data = user_data.model_dump(
                exclude_unset=True
            )

            # Check Duplicate Email
            if "email" in update_data:

                for existing_user in users:

                    if (
                        existing_user["email"] == update_data["email"]
                        and existing_user["id"] != user_id
                    ):

                        raise HTTPException(
                            status_code=409,
                            detail="Email already exists"
                        )

            # Update User Fields
            for key, value in update_data.items():

                if value is not None:
                    user[key] = value

            return {
                "message": "User updated successfully",
                "data": user
            }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


@router_v2.delete(
    "/user/{user_id}",
    response_model=UserDeleteResponse,
    status_code=status.HTTP_200_OK
)
async def delete_user(user_id: int):

    await asyncio.sleep(0)

    for user in users:

        if user["id"] == user_id:

            users.remove(user)

            return {
                "message": "User deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

