from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.base import ApiResponse, CamelCaseModel


class MenuBase(CamelCaseModel):
    """菜单基础模型"""
    name: str
    path: Optional[str] = None
    component: Optional[str] = None
    redirect: Optional[str] = None
    title: str
    icon: Optional[str] = None
    sort: int = 1
    is_hide: bool = False
    is_keep_alive: bool = True
    is_iframe: bool = False
    link: Optional[str] = None
    is_enable: bool = True
    menu_type: str = "menu"
    parent_id: Optional[int] = None
    roles: Optional[str] = None
    auth_name: Optional[str] = None
    auth_mark: Optional[str] = None
    auth_sort: int = 1


class MenuCreate(MenuBase):
    """创建菜单模型"""
    create_by: Optional[str] = None


class MenuUpdate(CamelCaseModel):
    """更新菜单模型"""
    name: Optional[str] = None
    path: Optional[str] = None
    component: Optional[str] = None
    redirect: Optional[str] = None
    title: Optional[str] = None
    icon: Optional[str] = None
    sort: Optional[int] = None
    is_hide: Optional[bool] = None
    is_keep_alive: Optional[bool] = None
    is_iframe: Optional[bool] = None
    link: Optional[str] = None
    is_enable: Optional[bool] = None
    menu_type: Optional[str] = None
    parent_id: Optional[int] = None
    roles: Optional[str] = None
    auth_name: Optional[str] = None
    auth_mark: Optional[str] = None
    auth_sort: Optional[int] = None
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
