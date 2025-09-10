# 公共CRUD操作函数，提供通用的CRUD操作辅助函数

from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User


def handle_user_role_association(
    db: Session, user: User, role_codes: List[str], operation: str = "assign"
) -> None:
    """处理用户角色关联"""
    if operation == "clear":
        user.roles.clear()
    elif operation == "assign" and role_codes:
        roles = db.query(Role).filter(Role.role_code.in_(role_codes)).all()
        if roles:
            user.roles.extend(roles)
    db.commit()


def create_with_audit(
    db: Session,
    crud,
    data: Dict[str, Any],
    current_user: User,
    operation: str = "create",
) -> Any:
    """创建记录并设置审计字段"""
    from app.core.response_helpers import set_audit_fields

    data = set_audit_fields(data, current_user, operation)
    return crud.create(db, data)


def update_with_audit(
    db: Session,
    crud,
    record: Any,
    data: Dict[str, Any],
    current_user: User,
    operation: str = "update",
) -> Any:
    """更新记录并设置审计字段"""
    from app.core.response_helpers import set_audit_fields

    data = set_audit_fields(data, current_user, operation)
    return crud.update(db, record, data)


def validate_and_create(
    db: Session,
    crud,
    data: Dict[str, Any],
    current_user: User,
    validators: List[callable] = None,
) -> Any:
    """验证并创建记录"""
    if validators:
        for validator in validators:
            validator(db, data)
    return create_with_audit(db, crud, data, current_user, "create")


def validate_and_update(
    db: Session,
    crud,
    record: Any,
    data: Dict[str, Any],
    current_user: User,
    validators: List[callable] = None,
) -> Any:
    """验证并更新记录"""
    if validators:
        for validator in validators:
            validator(db, data, record.id)
    return update_with_audit(db, crud, record, data, current_user, "update")


def build_filter_query(query, filters: Dict[str, Any]) -> Any:
    """构建过滤查询"""
    for field, value in filters.items():
        if value is not None:
            if hasattr(query.column_descriptions[0]["entity"], field):
                column = getattr(query.column_descriptions[0]["entity"], field)
                if isinstance(value, str):
                    query = query.filter(column.ilike(f"%{value}%"))
                else:
                    query = query.filter(column == value)
    return query


def get_or_create_default_admin(db: Session, user_crud) -> User:
    """获取或创建默认超级管理员"""
    existing_admin = (
        db.query(user_crud.model).filter(user_crud.model.user_name == "Super").first()
    )

    if not existing_admin:
        admin_data = {
            "email": "super@example.com",
            "phone": "18888888888",
            "user_name": "Super",
            "nick_name": "超级管理员",
            "password": "Super@3000",
            "status": True,
            "created_by": "system",
        }
        created_user = user_crud.create(db, admin_data)

        super_role = db.query(Role).filter(Role.role_code == "SUPER").first()
        if super_role and created_user:
            created_user.roles.append(super_role)
            db.commit()

        return created_user

    return existing_admin
