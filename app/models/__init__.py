# 导入所有模型以确保它们被注册到Base.metadata
from .user import User
from .role import Role
from .menu import Menu
from .dictionary import DictionaryType, DictionaryEnum
from .system import SystemSetting
from .order import InternalOrder, InternalOrderDetail, ExternalOrder, ExternalOrderDetail
from .user_role import user_role
from .role_menu import role_menu

__all__ = [
    "User",
    "Role", 
    "Menu",
    "DictionaryType",
    "DictionaryEnum",
    "SystemSetting",
    "InternalOrder",
    "InternalOrderDetail", 
    "ExternalOrder",
    "ExternalOrderDetail",
    "user_role",
    "role_menu"
]
