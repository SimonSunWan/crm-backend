#!/usr/bin/env python3
"""
角色菜单关联关系初始化脚本
用于建立超级管理员角色与所有菜单的关联关系
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.role import Role
from app.models.menu import Menu


def init_role_menu_relations():
    """初始化角色菜单关联关系"""
    db = SessionLocal()
    try:
        # 获取超级管理员角色
        super_role = db.query(Role).filter(Role.role_code == "SUPER").first()
        if not super_role:
            return

        # 获取所有菜单
        all_menus = db.query(Menu).all()
        if not all_menus:
            return

        # 检查是否已有关联关系
        existing_relations = len(super_role.menus)
        if existing_relations > 0:
            return

        # 建立超级管理员与所有菜单的关联关系
        super_role.menus.extend(all_menus)
        
        db.commit()
        
    except Exception as e:
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_role_menu_relations()
