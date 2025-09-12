#!/usr/bin/env python3
"""菜单数据初始化脚本"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.menu import Menu


def init_menu():
    """初始化菜单数据"""
    db = SessionLocal()
    try:
        # 检查是否已有菜单数据
        existing_menus = db.query(Menu).count()
        if existing_menus > 0:
            return

        # 创建基础菜单数据（移除硬编码的ID）
        menus_data = [
            # 工单管理
            {
                "name": "工单管理",
                "path": "/order",
                "icon": "&#xe70f;",
                "sort": 1,
                "is_hide": False,
                "is_keep_alive": False,
                "is_link": False,
                "is_enable": True,
                "menu_type": "menu",
                "parent_id": None,
                "auth_mark": None,
            },
            # 保内工单
            {
                "name": "保内工单",
                "path": "/order/internal",
                "icon": "",
                "sort": 1,
                "is_hide": False,
                "is_keep_alive": False,
                "is_link": False,
                "is_enable": True,
                "menu_type": "menu",
                "parent_id": None,  # 先设为None，后面会更新
                "auth_mark": None,
            },
            # 保外工单
            {
                "name": "保外工单",
                "path": "/order/external",
                "icon": "",
                "sort": 2,
                "is_hide": False,
                "is_keep_alive": False,
                "is_link": False,
                "is_enable": True,
                "menu_type": "menu",
                "parent_id": None,  # 先设为None，后面会更新
                "auth_mark": None,
            },
            # 系统管理
            {
                "name": "系统管理",
                "path": "/system",
                "icon": "&#xe7b9;",
                "sort": 2,
                "is_hide": False,
                "is_keep_alive": False,
                "is_link": False,
                "is_enable": True,
                "menu_type": "menu",
                "parent_id": None,
                "auth_mark": None,
            },
            # 个人中心
            {
                "name": "个人中心",
                "path": "/system/user-center",
                "icon": "",
                "sort": 1,
                "is_hide": False,
                "is_keep_alive": False,
                "is_link": False,
                "is_enable": True,
                "menu_type": "menu",
                "parent_id": None,  # 先设为None，后面会更新
                "auth_mark": None,
            },
            # 用户管理
            {
                "name": "用户管理",
                "path": "/system/user",
                "icon": "",
                "sort": 2,
                "is_hide": False,
                "is_keep_alive": False,
                "is_link": False,
                "is_enable": True,
                "menu_type": "menu",
                "parent_id": None,  # 先设为None，后面会更新
                "auth_mark": None,
            },
            # 角色管理
            {
                "name": "角色管理",
                "path": "/system/role",
                "icon": "",
                "sort": 3,
                "is_hide": False,
                "is_keep_alive": False,
                "is_link": False,
                "is_enable": True,
                "menu_type": "menu",
                "parent_id": None,  # 先设为None，后面会更新
                "auth_mark": None,
            },
            # 菜单管理
            {
                "name": "菜单管理",
                "path": "/system/menu",
                "icon": "",
                "sort": 4,
                "is_hide": False,
                "is_keep_alive": False,
                "is_link": False,
                "is_enable": True,
                "menu_type": "menu",
                "parent_id": None,  # 先设为None，后面会更新
                "auth_mark": None,
            },
            # 字典管理
            {
                "name": "字典管理",
                "path": "/system/dictionary",
                "icon": "",
                "sort": 5,
                "is_hide": False,
                "is_keep_alive": False,
                "is_link": False,
                "is_enable": True,
                "menu_type": "menu",
                "parent_id": None,  # 先设为None，后面会更新
                "auth_mark": None,
            },
        ]

        # 创建菜单并获取生成的ID
        created_menus = {}
        for menu_data in menus_data:
            menu = Menu(**menu_data)
            db.add(menu)
            db.flush()  # 刷新以获取生成的ID
            created_menus[menu_data["name"]] = menu.id

        # 创建按钮权限数据
        button_data = [
            # 保内工单 - 查看全部按钮
            {
                "name": "保内查看全部",
                "path": "",
                "icon": "",
                "sort": 2,
                "is_hide": False,
                "is_keep_alive": False,
                "is_link": False,
                "is_enable": True,
                "menu_type": "button",
                "parent_id": created_menus["保内工单"],
                "auth_mark": "view_all",
            },
            # 保外工单 - 查看全部按钮
            {
                "name": "保外查看全部",
                "path": "",
                "icon": "",
                "sort": 2,
                "is_hide": False,
                "is_keep_alive": False,
                "is_link": False,
                "is_enable": True,
                "menu_type": "button",
                "parent_id": created_menus["保外工单"],
                "auth_mark": "view_all",
            },
        ]

        # 插入按钮数据
        for button in button_data:
            menu = Menu(**button)
            db.add(menu)

        # 更新子菜单的parent_id
        # 保内工单和保外工单的父级是工单管理
        internal_order_menu = db.query(Menu).filter(Menu.name == "保内工单").first()
        external_order_menu = db.query(Menu).filter(Menu.name == "保外工单").first()
        order_management_menu = db.query(Menu).filter(Menu.name == "工单管理").first()

        if internal_order_menu and order_management_menu:
            internal_order_menu.parent_id = order_management_menu.id
        if external_order_menu and order_management_menu:
            external_order_menu.parent_id = order_management_menu.id

        # 系统管理下的子菜单
        system_menu = db.query(Menu).filter(Menu.name == "系统管理").first()
        system_submenus = ["个人中心", "用户管理", "角色管理", "菜单管理", "字典管理"]

        for submenu_name in system_submenus:
            submenu = db.query(Menu).filter(Menu.name == submenu_name).first()
            if submenu and system_menu:
                submenu.parent_id = system_menu.id

        # 提交事务
        db.commit()

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_menu()
