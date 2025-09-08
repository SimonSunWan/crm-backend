from pydantic import BaseModel, field_serializer
from typing import Optional, Any, List
from datetime import datetime
from app.schemas.base import ApiResponse, Token, CamelCaseModel
from app.schemas.role import RoleResponse


class UserBase(CamelCaseModel):

    email: Optional[str] = None
    phone: Optional[str] = None
    user_name: str
    nick_name: Optional[str] = None
    avatar: Optional[str] = None  # 头像URL
    status: bool
    roles: List[str]  # 角色编码数组


class UserCreate(UserBase):

    password: str


class UserUpdate(CamelCaseModel):

    email: Optional[str] = None
    phone: Optional[str] = None
    user_name: Optional[str] = None
    nick_name: Optional[str] = None
    avatar: Optional[str] = None  # 头像URL
    status: Optional[bool] = None
    roles: Optional[List[str]] = None  # 角色编码数组


class UserResponse(UserBase):

    id: int
    create_by: Optional[str] = None
    create_time: Optional[datetime] = None
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None
    role_names: Optional[List[str]] = None  # 角色名称数组

    @field_serializer('create_time', 'update_time')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """序列化datetime为yyyy-MM-dd HH:mm:ss格式"""
        if value is None:
            return None
        return value.strftime('%Y-%m-%d %H:%M:%S')

    model_config = {"exclude": {"hashed_password"}}

    @classmethod
    def model_validate(cls, obj):
        """重写验证方法，处理角色数据转换"""
        # 创建数据字典，避免直接修改原对象
        data = {}
        
        # 复制基本字段
        for field in ['id', 'email', 'phone', 'user_name', 'nick_name', 'avatar', 'create_by', 'create_time', 'update_by', 'update_time']:
            if hasattr(obj, field):
                data[field] = getattr(obj, field)
        
        # 处理角色数据
        if hasattr(obj, 'roles'):
            role_codes = [role.role_code for role in obj.roles] if obj.roles else []
            role_names = [role.role_name for role in obj.roles] if obj.roles else []
            data['roles'] = role_codes
            data['role_names'] = role_names
        else:
            data['roles'] = []
            data['role_names'] = []
        
        # 处理status字段：将字符串转换为布尔值
        if hasattr(obj, 'status') and obj.status is not None:
            data['status'] = obj.status == '1'
        else:
            data['status'] = True  # 默认值
        
        return super().model_validate(data)


class UserLogin(CamelCaseModel):
    user_name: str
    password: str


class UserRegister(CamelCaseModel):
    user_name: str
    nick_name: str
    phone: str
    email: Optional[str] = None
    password: str
    system_code: str


class UserForgetPassword(CamelCaseModel):
    username: str
    new_password: str
    system_code: str


class LoginResponse(ApiResponse):
    data: Token
