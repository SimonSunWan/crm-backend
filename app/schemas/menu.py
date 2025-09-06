from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.base import ApiResponse, CamelCaseModel


# 前向引用声明
class RoleResponseForMenu(BaseModel):
    id: int
    role_name: str
    role_code: str
    description: Optional[str] = None
    status: bool = True


class MenuBase(CamelCaseModel):
    """菜单基础模型"""
    name: str
    path: Optional[str] = None
    icon: Optional[str] = None
    sort: int = 1
    is_hide: bool = False
    is_keep_alive: bool = True
    is_link: bool = False
    link: Optional[str] = None
    is_enable: bool = True
    menu_type: str = "menu"
    parent_id: Optional[int] = None
    roles: Optional[List[RoleResponseForMenu]] = None
    auth_mark: Optional[str] = None


class MenuCreate(CamelCaseModel):
    """创建菜单模型"""
    name: str
    path: Optional[str] = None
    icon: Optional[str] = None
    sort: int = 1
    is_hide: bool = False
    is_keep_alive: bool = True
    is_link: bool = False
    link: Optional[str] = None
    is_enable: bool = True
    menu_type: str = "menu"
    parent_id: Optional[int] = None
    auth_mark: Optional[str] = None
    create_by: Optional[str] = None


class MenuUpdate(CamelCaseModel):
    """更新菜单模型"""
    name: Optional[str] = None
    path: Optional[str] = None
    icon: Optional[str] = None
    sort: Optional[int] = None
    is_hide: Optional[bool] = None
    is_keep_alive: Optional[bool] = None
    is_link: Optional[bool] = None
    link: Optional[str] = None
    is_enable: Optional[bool] = None
    menu_type: Optional[str] = None
    parent_id: Optional[int] = None
    auth_mark: Optional[str] = None
    update_by: Optional[str] = None


class MenuResponse(MenuBase):
    """菜单响应模型"""
    id: int
    create_by: Optional[str] = None
    create_time: Optional[datetime] = None
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None
    children: Optional[List['MenuResponse']] = None


# 解决循环引用
MenuResponse.model_rebuild()
