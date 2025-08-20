from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.base import ApiResponse, CamelCaseModel


class RoleBase(CamelCaseModel):
    """角色基础模型"""
    role_name: str
    role_code: str
    description: Optional[str] = None
    status: bool = True


class RoleCreate(RoleBase):
    """创建角色模型"""
    pass


class RoleUpdate(CamelCaseModel):
    """更新角色模型"""
    role_name: Optional[str] = None
    role_code: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None


class RoleResponse(RoleBase):
    """角色响应模型"""
    id: int
    create_by: Optional[str] = None
    create_time: Optional[datetime] = None
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None
