from pydantic import BaseModel, EmailStr
from typing import Optional, Any, List
from datetime import datetime
from app.schemas.base import ApiResponse, Token


class UserBase(BaseModel):

    email: EmailStr
    phone: Optional[str] = None
    user_name: str
    full_name: Optional[str] = None
    is_active: bool = True
    roles: List[str]


class UserCreate(UserBase):

    password: str


class UserUpdate(BaseModel):

    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    user_name: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    roles: Optional[List[str]] = None


class UserResponse(UserBase):

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True, "exclude": {"hashed_password"}}


class UserLogin(BaseModel):
    user_name: str
    password: str


class LoginResponse(ApiResponse):
    data: Token
