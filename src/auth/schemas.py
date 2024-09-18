from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    user = "user"
    reviewer = "reviewer"
    admin = "admin"

class UserBase(BaseModel):
    full_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id_user: int
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password_hash: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    username: EmailStr
    password: str