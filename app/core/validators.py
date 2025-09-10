# 公共验证函数，提供各种业务验证的公共函数

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.exceptions import InvalidSystemCodeError
from app.crud.system import system_setting_crud


def validate_system_code(
    db: Session, system_code: str, setting_key: str = "REGISTER_SYSTEM_CODE"
) -> bool:
    """验证系统码"""
    system_code_setting = system_setting_crud.get_by_key(db, setting_key=setting_key)
    if not system_code_setting or system_code_setting.setting_value != system_code:
        raise InvalidSystemCodeError("系统码错误")
    return True


def validate_uniqueness(
    db: Session,
    crud,
    field_name: str,
    field_value: str,
    get_method: str,
    error_message: str,
    exclude_id: int = None,
) -> bool:
    """通用唯一性验证函数"""
    if not field_value:
        return True

    get_func = getattr(crud, get_method)
    existing_record = get_func(db, field_value)

    if existing_record and (exclude_id is None or existing_record.id != exclude_id):
        raise HTTPException(status_code=400, detail=error_message)
    return True


def validate_email_uniqueness(
    db: Session, email: str, user_crud, exclude_user_id: int = None
) -> bool:
    """验证邮箱唯一性"""
    return validate_uniqueness(
        db, user_crud, "email", email, "get_by_email", "邮箱已存在", exclude_user_id
    )


def validate_username_uniqueness(
    db: Session, username: str, user_crud, exclude_user_id: int = None
) -> bool:
    """验证用户名唯一性"""
    return validate_uniqueness(
        db,
        user_crud,
        "user_name",
        username,
        "get_by_username",
        "用户名已存在",
        exclude_user_id,
    )


def validate_role_name_uniqueness(
    db: Session, role_name: str, role_crud, exclude_role_id: int = None
) -> bool:
    """验证角色名称唯一性"""
    return validate_uniqueness(
        db,
        role_crud,
        "role_name",
        role_name,
        "get_by_name",
        "角色名称已存在",
        exclude_role_id,
    )


def validate_role_code_uniqueness(
    db: Session, role_code: str, role_crud, exclude_role_id: int = None
) -> bool:
    """验证角色编码唯一性"""
    return validate_uniqueness(
        db,
        role_crud,
        "role_code",
        role_code,
        "get_by_code",
        "角色编码已存在",
        exclude_role_id,
    )


def validate_menu_name_uniqueness(
    db: Session, menu_name: str, parent_id: int, menu_crud, exclude_menu_id: int = None
) -> bool:
    """验证菜单名称唯一性（同层级）"""
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
    """验证菜单路径唯一性"""
    return validate_uniqueness(
        db,
        menu_crud,
        "menu_path",
        menu_path,
        "get_by_path",
        "路由路径已存在",
        exclude_menu_id,
    )


def validate_menu_auth_mark_uniqueness(
    db: Session, auth_mark: str, parent_id: int, menu_crud, exclude_menu_id: int = None
) -> bool:
    """验证菜单权限标识唯一性（同层级）"""
    if not auth_mark:
        return True

    existing_menu = menu_crud.get_by_auth_mark_and_parent(db, auth_mark, parent_id)
    if existing_menu and (
        exclude_menu_id is None or existing_menu.id != exclude_menu_id
    ):
        raise HTTPException(status_code=400, detail="权限标识已存在")
    return True
