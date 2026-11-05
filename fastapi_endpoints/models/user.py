from pydantic import BaseModel , Field ,EmailStr

# Create data validation and error message : - 

# Create a users 
class Usercreate (BaseModel) : 
    name: str = Field(...,description="Full name of the user",examples=["Rahul Sharma"])
    age: int = Field(...,description="Age of the user",examples=[25])
    email: EmailStr = Field(...,description="Registered email address",examples=["rahul@gmail.com"])
    phone: str | None = Field(default=None,description="Registered contact number",examples=["9876543210"])
    is_active: bool = Field(...,description="Indicates whether the user account is active",examples=[True])
    

# Create User Response
class UserResponse(BaseModel):

    id: int = Field(...,description="Unique ID assigned to the user",examples=[1])
    name: str = Field(...,description="Full name of the user",examples=["Rahul Sharma"])
    age: int = Field(...,description="Age of the user",examples=[25])
    email: EmailStr = Field(...,description="Registered email address",examples=["rahul@gmail.com"])
    phone: str | None = Field(default=None,description="Registered contact number",examples=["9876543210"])
    is_active: bool = Field(...,description="Indicates whether the user account is active",examples=[True])


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
    age: int | None = Field(default=None,ge=18,le=100,description="Updated age of the user (18-100)",examples=[25])
    email: EmailStr | None = Field(default=None,description="Updated valid email address",examples=["rahul@gmail.com"])
    phone: str | None = Field(default=None,min_length=10,max_length=15,description="Updated contact number",examples=["9876543210"])
    is_active: bool | None = Field(default=None,description="Updated account active status",examples=[True])





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



