from pydantic  import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    is_active: bool = True

    class Config:
        orm_mode = True
        from_attributes = True
