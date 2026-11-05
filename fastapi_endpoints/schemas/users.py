from pydantic import BaseModel , Field ,EmailStr

class Usercreate (BaseModel) : 
    name : str = Field(...,min_length=2,max_length=50,description="User name must contain 2-50 characters")
    email : EmailStr = Field(...,description="Enter a valid email address")
    age : int = Field(...,ge=18,le=100,description="Age must be between 18 and 100")
    phone : str = Field(...,default=None,min_length=10,max_length=15)
    is_active : bool = Field(...,default=True,description="User account status")

    