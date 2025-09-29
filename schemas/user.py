from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from models import Role

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    password: str = Field(..., min_length=8, max_length=100) 
    
class User(UserBase):
    id: int
    role: Role
    created_at: datetime

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role
    created_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None