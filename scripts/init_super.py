#!/usr/bin/env python3
"""
超级管理员初始化脚本
用于在数据库创建后插入超级管理员角色和用户
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.crud.user import user_crud
from app.models.role import Role
from app.models.user import User


def init_super():
    """初始化超级管理员角色和用户"""
    db = SessionLocal()
    try:
        # 检查是否已存在超级管理员角色
        existing_super_role = db.query(Role).filter(Role.role_code == "SUPER").first()
        if not existing_super_role:
            # 创建超级管理员角色
            role_data = {
                "role_name": "超级管理员",
                "role_code": "SUPER",
                "description": "系统超级管理员，拥有所有权限",
                "status": True,
                "created_by": "system",
            }
            super_role = Role(**role_data)
            db.add(super_role)
            db.commit()
            db.refresh(super_role)
        else:
            super_role = existing_super_role

        # 检查是否已存在超级管理员用户
        existing_super_user = db.query(User).filter(User.user_name == "admin").first()
        if not existing_super_user:
            # 创建超级管理员用户
            user_data = {
                "user_name": "Super",
                "nick_name": "超级管理员",
                "email": "super@example.com",
                "password": "Super@3000",
                "status": True,
                "created_by": "system",
            }
            super_user = user_crud.create(db, user_data)

            # 关联用户和角色
            super_user.roles.append(super_role)
            db.commit()
        else:
            # 如果用户已存在但未关联超级管理员角色，则关联
            if super_role not in existing_super_user.roles:
                existing_super_user.roles.append(super_role)
                db.commit()

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_super()
