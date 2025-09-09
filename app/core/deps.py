from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.exceptions import InvalidTokenError, UserDisabledError
from app.models.user import User


def get_current_user_dependency(
    authorization: str = Header(..., description="Bearer token"),
    db: Session = Depends(get_db)
) -> User:
    """获取当前登录用户的依赖注入函数"""
    if not authorization.startswith("Bearer "):
        raise InvalidTokenError("无效的认证头格式")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)
    
    if not user:
        raise InvalidTokenError("无效的token或用户不存在")
    
    if user.status != '1':
        raise UserDisabledError("用户未启用")
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user_dependency)
) -> User:
    """获取当前活跃用户的依赖注入函数"""
    return current_user


def get_current_superuser(
    current_user: User = Depends(get_current_user_dependency)
) -> User:
    """获取当前超级用户的依赖注入函数"""
    from app.models.role import Role
    super_role = next((role for role in current_user.roles if role.role_code == "SUPER"), None)
    if not super_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要超级管理员权限"
        )
    return current_user
