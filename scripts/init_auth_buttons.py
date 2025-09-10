#!/usr/bin/env python3
"""
权限按钮数据初始化脚本
用于在数据库创建后插入基础的权限按钮数据
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.menu import Menu


def init_auth_buttons():
    """初始化权限按钮数据"""
    db = SessionLocal()
    try:
        # 检查是否已有权限按钮数据
        existing_auth_buttons = (
            db.query(Menu).filter(Menu.menu_type == "button").count()
        )
        if existing_auth_buttons > 0:
            return

        # 获取现有的菜单，为它们添加权限按钮
        existing_menus = db.query(Menu).filter(Menu.menu_type == "menu").all()

        # 为每个菜单添加权限按钮
        auth_buttons_data = []
        for menu in existing_menus:
            # 为每个菜单添加增删改查权限
            auth_buttons_data.extend(
                [
                    {
                        "name": f"{menu.title}_新增",
                        "path": "",
                        "component": "",
                        "title": f"{menu.title}_新增",
                        "icon": "",
                        "sort": 1,
                        "menu_type": "button",
                        "parent_id": menu.id,
                        "auth_name": f"{menu.title}_新增",
                        "auth_mark": "add",
                        "auth_sort": 1,
                        "is_enable": True,
                    },
                    {
                        "name": f"{menu.title}_编辑",
                        "path": "",
                        "component": "",
                        "title": f"{menu.title}_编辑",
                        "icon": "",
                        "sort": 2,
                        "menu_type": "button",
                        "parent_id": menu.id,
                        "auth_name": f"{menu.title}_编辑",
                        "auth_mark": "edit",
                        "auth_sort": 2,
                        "is_enable": True,
                    },
                    {
                        "name": f"{menu.title}_删除",
                        "path": "",
                        "component": "",
                        "title": f"{menu.title}_删除",
                        "icon": "",
                        "sort": 3,
                        "menu_type": "button",
                        "parent_id": menu.id,
                        "auth_name": f"{menu.title}_删除",
                        "auth_mark": "delete",
                        "auth_sort": 3,
                        "is_enable": True,
                    },
                    {
                        "name": f"{menu.title}_查看",
                        "path": "",
                        "component": "",
                        "title": f"{menu.title}_查看",
                        "icon": "",
                        "sort": 4,
                        "menu_type": "button",
                        "parent_id": menu.id,
                        "auth_name": f"{menu.title}_查看",
                        "auth_mark": "view",
                        "auth_sort": 4,
                        "is_enable": True,
                    },
                ]
            )

        # 插入权限按钮数据
        for auth_button_data in auth_buttons_data:
            auth_button = Menu(**auth_button_data)
            db.add(auth_button)

        # 提交事务
        db.commit()

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_auth_buttons()
