#!/usr/bin/env python3
"""
角色数据初始化脚本
用于在数据库创建后插入基础的角色数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.role import Role


def init_roles():
    """初始化角色数据"""
    db = SessionLocal()
    try:
        # 检查是否已有角色数据
        existing_roles = db.query(Role).count()
        if existing_roles > 0:
            return

        # 创建基础角色数据
        roles_data = [
            {
                "role_name": "超级管理员",
                "role_code": "SUPER",
                "description": "系统超级管理员，拥有所有权限",
                "status": True,
                "create_by": "system"
            },
            {
                "role_name": "管理员",
                "role_code": "ADMIN",
                "description": "系统管理员，拥有大部分权限",
                "status": True,
                "create_by": "system"
            },
            {
                "role_name": "普通用户",
                "role_code": "USER",
                "description": "普通用户，拥有基本权限",
                "status": True,
                "create_by": "system"
            }
        ]

        # 插入角色数据
        for role_data in roles_data:
            role = Role(**role_data)
            db.add(role)

        db.commit()
        
    except Exception as e:
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_roles()
