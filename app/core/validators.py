"""
公共验证函数
提供各种业务验证的公共函数
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.exceptions import InvalidSystemCodeError, UserAlreadyExistsError
from app.crud.system import system_setting_crud


def validate_system_code(
    db: Session, system_code: str, setting_key: str = "REGISTER_SYSTEM_CODE"
) -> bool:
    """
    验证系统码

    Args:
        db: 数据库会话
        system_code: 用户输入的系统码
        setting_key: 系统设置键名

    Returns:
        bool: 验证是否通过

    Raises:
        InvalidSystemCodeError: 系统码错误
    """
    system_code_setting = system_setting_crud.get_by_key(db, setting_key=setting_key)
    if not system_code_setting or system_code_setting.setting_value != system_code:
        raise InvalidSystemCodeError("系统码错误")
    return True


def validate_email_uniqueness(
    db: Session, email: str, user_crud, exclude_user_id: int = None
) -> bool:
    """
    验证邮箱唯一性

    Args:
        db: 数据库会话
        email: 邮箱地址
        user_crud: 用户CRUD对象
        exclude_user_id: 排除的用户ID（用于更新时排除自己）

    Returns:
        bool: 验证是否通过

    Raises:
        UserAlreadyExistsError: 邮箱已存在
    """
    if not email:
        return True

    existing_user = user_crud.get_by_email(db, email)
    if existing_user and (
        exclude_user_id is None or existing_user.id != exclude_user_id
    ):
        raise UserAlreadyExistsError("邮箱已存在")
    return True


def validate_username_uniqueness(
    db: Session, username: str, user_crud, exclude_user_id: int = None
) -> bool:
    """
    验证用户名唯一性

    Args:
        db: 数据库会话
        username: 用户名
        user_crud: 用户CRUD对象
        exclude_user_id: 排除的用户ID（用于更新时排除自己）

    Returns:
        bool: 验证是否通过

    Raises:
        UserAlreadyExistsError: 用户名已存在
    """
    if not username:
        return True

    existing_user = user_crud.get_by_username(db, username)
    if existing_user and (
        exclude_user_id is None or existing_user.id != exclude_user_id
    ):
        raise UserAlreadyExistsError("用户名已存在")
    return True


def validate_role_name_uniqueness(
    db: Session, role_name: str, role_crud, exclude_role_id: int = None
) -> bool:
    """
    验证角色名称唯一性

    Args:
        db: 数据库会话
        role_name: 角色名称
        role_crud: 角色CRUD对象
        exclude_role_id: 排除的角色ID（用于更新时排除自己）

    Returns:
        bool: 验证是否通过

    Raises:
        HTTPException: 角色名称已存在
    """
    if not role_name:
        return True

    existing_role = role_crud.get_by_name(db, role_name)
    if existing_role and (
        exclude_role_id is None or existing_role.id != exclude_role_id
    ):
        raise HTTPException(status_code=400, detail="角色名称已存在")
    return True


def validate_role_code_uniqueness(
    db: Session, role_code: str, role_crud, exclude_role_id: int = None
) -> bool:
    """
    验证角色编码唯一性

    Args:
        db: 数据库会话
        role_code: 角色编码
        role_crud: 角色CRUD对象
        exclude_role_id: 排除的角色ID（用于更新时排除自己）

    Returns:
        bool: 验证是否通过

    Raises:
        HTTPException: 角色编码已存在
    """
    if not role_code:
        return True

    existing_role = role_crud.get_by_code(db, role_code)
    if existing_role and (
        exclude_role_id is None or existing_role.id != exclude_role_id
    ):
        raise HTTPException(status_code=400, detail="角色编码已存在")
    return True


def validate_menu_name_uniqueness(
    db: Session, menu_name: str, parent_id: int, menu_crud, exclude_menu_id: int = None
) -> bool:
    """
    验证菜单名称唯一性（同层级）

    Args:
        db: 数据库会话
        menu_name: 菜单名称
        parent_id: 父菜单ID
        menu_crud: 菜单CRUD对象
        exclude_menu_id: 排除的菜单ID（用于更新时排除自己）

    Returns:
        bool: 验证是否通过

    Raises:
        HTTPException: 菜单名称已存在
    """
    if not menu_name:
        return True

    existing_menu = menu_crud.get_by_name_and_parent(db, menu_name, parent_id)
    if existing_menu and (
        exclude_menu_id is None or existing_menu.id != exclude_menu_id
    ):
        raise HTTPException(status_code=400, detail="菜单名称已存在")
    return True


def validate_menu_path_uniqueness(
    db: Session, menu_path: str, menu_crud, exclude_menu_id: int = None
) -> bool:
    """
    验证菜单路径唯一性

    Args:
        db: 数据库会话
        menu_path: 菜单路径
        menu_crud: 菜单CRUD对象
        exclude_menu_id: 排除的菜单ID（用于更新时排除自己）

    Returns:
        bool: 验证是否通过

    Raises:
        HTTPException: 路由路径已存在
    """
    if not menu_path:
        return True

    existing_menu = menu_crud.get_by_path(db, menu_path)
    if existing_menu and (
        exclude_menu_id is None or existing_menu.id != exclude_menu_id
    ):
        raise HTTPException(status_code=400, detail="路由路径已存在")
    return True


def validate_menu_auth_mark_uniqueness(
    db: Session, auth_mark: str, parent_id: int, menu_crud, exclude_menu_id: int = None
) -> bool:
    """
    验证菜单权限标识唯一性（同层级）

    Args:
        db: 数据库会话
        auth_mark: 权限标识
        parent_id: 父菜单ID
        menu_crud: 菜单CRUD对象
        exclude_menu_id: 排除的菜单ID（用于更新时排除自己）

    Returns:
        bool: 验证是否通过

    Raises:
        HTTPException: 权限标识已存在
    """
    if not auth_mark:
        return True

    existing_menu = menu_crud.get_by_auth_mark_and_parent(db, auth_mark, parent_id)
    if existing_menu and (
        exclude_menu_id is None or existing_menu.id != exclude_menu_id
    ):
        raise HTTPException(status_code=400, detail="权限标识已存在")
    return True
