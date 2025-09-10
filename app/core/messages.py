"""统一响应消息管理"""

from typing import Any

from app.schemas.base import ApiResponse


class Messages:
    """统一响应消息类"""

    # 通用成功消息
    SUCCESS = "操作成功"
    CREATED = "创建成功"
    UPDATED = "更新成功"
    DELETED = "删除成功"
    RETRIEVED = "获取成功"

    # 用户相关
    USER_LOGIN_SUCCESS = "登录成功"
    USER_LOGOUT_SUCCESS = "退出成功"
    USER_REGISTER_SUCCESS = "注册成功"
    USER_UPDATE_SUCCESS = "用户信息更新成功"
    PASSWORD_CHANGE_SUCCESS = "密码修改成功"

    # 菜单相关
    MENU_CREATE_SUCCESS = "菜单创建成功"
    MENU_UPDATE_SUCCESS = "菜单更新成功"
    MENU_DELETE_SUCCESS = "菜单删除成功"
    MENU_TREE_SUCCESS = "菜单树获取成功"

    # 角色相关
    ROLE_CREATE_SUCCESS = "角色创建成功"
    ROLE_UPDATE_SUCCESS = "角色更新成功"
    ROLE_DELETE_SUCCESS = "角色删除成功"

    # 工单相关
    ORDER_CREATE_SUCCESS = "工单创建成功"
    ORDER_UPDATE_SUCCESS = "工单更新成功"
    ORDER_DELETE_SUCCESS = "工单删除成功"

    # 字典相关
    DICTIONARY_CREATE_SUCCESS = "字典创建成功"
    DICTIONARY_UPDATE_SUCCESS = "字典更新成功"
    DICTIONARY_DELETE_SUCCESS = "字典删除成功"

    # 系统相关
    SYSTEM_CONFIG_SUCCESS = "系统配置获取成功"
    SYSTEM_CONFIG_UPDATE_SUCCESS = "系统配置更新成功"

    # 缓存相关
    CACHE_CLEAR_SUCCESS = "缓存清除成功"
    CACHE_REFRESH_SUCCESS = "缓存刷新成功"


def success_response(
    message: str = Messages.SUCCESS, data: Any = None, code: int = 200
) -> ApiResponse:
    """创建成功响应"""
    return ApiResponse(code=code, message=message, data=data)


def created_response(message: str = Messages.CREATED, data: Any = None) -> ApiResponse:
    """创建成功响应（201状态码）"""
    return ApiResponse(code=201, message=message, data=data)


def updated_response(message: str = Messages.UPDATED, data: Any = None) -> ApiResponse:
    """更新成功响应"""
    return ApiResponse(code=200, message=message, data=data)


def deleted_response(message: str = Messages.DELETED) -> ApiResponse:
    """删除成功响应"""
    return ApiResponse(code=200, message=message)


def retrieved_response(
    message: str = Messages.RETRIEVED, data: Any = None
) -> ApiResponse:
    """获取成功响应"""
    return ApiResponse(code=200, message=message, data=data)
