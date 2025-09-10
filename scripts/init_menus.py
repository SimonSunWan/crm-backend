#!/usr/bin/env python3
"""
菜单数据初始化脚本
用于在数据库创建后插入基础的菜单数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.menu import Menu


def init_menus():
    """初始化菜单数据"""
    db = SessionLocal()
    try:
        # 检查是否已有菜单数据
        existing_menus = db.query(Menu).count()
        if existing_menus > 0:
            return

        # 创建基础菜单数据
        menus_data = [
            # 仪表板
            {
                "name": "Dashboard",
                "path": "/dashboard",
                "component": "Layout",
                "title": "仪表板",
                "icon": "&#xe721;",
                "sort": 1,
                "menu_type": "menu",
                "parent_id": None,
                "roles": "SUPER"
            },
            {
                "name": "Console",
                "path": "console",
                "component": "Dashboard",
                "title": "控制台",
                "icon": "",
                "sort": 1,
                "menu_type": "menu",
                "parent_id": 1,  # Dashboard的子菜单
                "roles": "SUPER"
            },
            # 系统管理
            {
                "name": "System",
                "path": "/system",
                "component": "Layout",
                "title": "系统管理",
                "icon": "&#xe7b9;",
                "sort": 2,
                "menu_type": "menu",
                "parent_id": None,
                "roles": "SUPER"
            },
            {
                "name": "User",
                "path": "user",
                "component": "User",
                "title": "用户管理",
                "icon": "",
                "sort": 1,
                "menu_type": "menu",
                "parent_id": 3,  # System的子菜单
                "roles": "SUPER"
            },
            {
                "name": "Role",
                "path": "role",
                "component": "Role",
                "title": "角色管理",
                "icon": "",
                "sort": 2,
                "menu_type": "menu",
                "parent_id": 3,  # System的子菜单
                "roles": "SUPER"
            },
            {
                "name": "UserCenter",
                "path": "user-center",
                "component": "UserCenter",
                "title": "个人中心",
                "icon": "",
                "sort": 3,
                "menu_type": "menu",
                "parent_id": 3,  # System的子菜单
                "is_hide": False,
                "roles": "SUPER"
            },
            {
                "name": "Menus",
                "path": "menu",
                "component": "Menu",
                "title": "菜单管理",
                "icon": "",
                "sort": 4,
                "menu_type": "menu",
                "parent_id": 3,  # System的子菜单
                "roles": "SUPER"
            },
            {
                "name": "Dictionary",
                "path": "dictionary",
                "component": "Dictionary",
                "title": "字典管理",
                "icon": "",
                "sort": 5,
                "menu_type": "menu",
                "parent_id": 3,  # System的子菜单
                "roles": "SUPER"
            },
            # 客户管理
            {
                "name": "Customer",
                "path": "/customer",
                "component": "Layout",
                "title": "客户管理",
                "icon": "&#xe7b9;",
                "sort": 3,
                "menu_type": "menu",
                "parent_id": None,
                "roles": "SUPER"
            },
            {
                "name": "CustomerList",
                "path": "list",
                "component": "Customer",
                "title": "客户列表",
                "icon": "",
                "sort": 1,
                "menu_type": "menu",
                "parent_id": 9,  # Customer的子菜单
                "roles": "SUPER"
            }
        ]

        # 插入菜单数据
        for menu_data in menus_data:
            menu = Menu(**menu_data)
            db.add(menu)

        # 提交事务
        db.commit()

    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_menus()
