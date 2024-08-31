from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="johndoe")
    email: EmailStr = Field(..., example="johndoe@example.com")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100, example="your_password")

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50, example="newusername")
    email: Optional[EmailStr] = Field(None, example="newemail@example.com")
    password: Optional[str] = Field(None, min_length=8, max_length=100, example="new_password")

class UserResponse(UserBase):
    id: int

class TokenData(BaseModel):
    token: str