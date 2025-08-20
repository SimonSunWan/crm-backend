from pydantic import BaseModel, EmailStr
from typing import Optional, Any, List
from datetime import datetime
from app.schemas.base import ApiResponse, Token, CamelCaseModel
from app.schemas.role import RoleResponse


class UserBase(CamelCaseModel):

    email: EmailStr
    phone: Optional[str] = None
    user_name: str
    nick_name: Optional[str] = None
    status: str
    roles: List[RoleResponse]


class UserCreate(UserBase):

    password: str


class UserUpdate(CamelCaseModel):

    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    user_name: Optional[str] = None
    nick_name: Optional[str] = None
    status: Optional[str] = None
    roles: Optional[List[RoleResponse]] = None


class UserResponse(UserBase):

    id: int
    create_by: Optional[str] = None
    create_time: Optional[datetime] = None
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None

    model_config = {"exclude": {"hashed_password"}}


class UserLogin(CamelCaseModel):
    user_name: str
    password: str


class LoginResponse(ApiResponse):
    data: Token
