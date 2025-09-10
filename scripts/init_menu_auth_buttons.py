#!/usr/bin/env python3
"""
菜单权限按钮初始化脚本
用于为菜单创建对应的权限按钮数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.menu import Menu


def init_menu_auth_buttons():
    """初始化菜单权限按钮数据"""
    db = SessionLocal()
    try:
        # 检查是否已有权限按钮数据
        existing_auth_buttons = db.query(Menu).filter(Menu.menu_type == "button").count()
        if existing_auth_buttons > 0:
            print(f"发现 {existing_auth_buttons} 个现有权限按钮，将重新创建")
            # 删除现有的权限按钮
            db.query(Menu).filter(Menu.menu_type == "button").delete()
            db.commit()

        # 获取所有菜单类型的菜单
        menu_items = db.query(Menu).filter(Menu.menu_type == "menu").all()
        
        # 为每个菜单创建权限按钮
        auth_buttons_data = []
        
        for menu in menu_items:
            # 为每个菜单创建基础的权限按钮
            auth_buttons = [
                {
                    "name": f"{menu.name}_add",
                    "path": f"{menu.path}/add",
                    "component": "",
                    "title": "新增",
                    "icon": "",
                    "sort": 1,
                    "menu_type": "button",
                    "parent_id": menu.id,
                    "roles": menu.roles,
                    "auth_name": "新增",
                    "auth_mark": "add",
                    "auth_sort": 1
                },
                {
                    "name": f"{menu.name}_edit",
                    "path": f"{menu.path}/edit",
                    "component": "",
                    "title": "编辑",
                    "icon": "",
                    "sort": 2,
                    "menu_type": "button",
                    "parent_id": menu.id,
                    "roles": menu.roles,
                    "auth_name": "编辑",
                    "auth_mark": "edit",
                    "auth_sort": 2
                },
                {
                    "name": f"{menu.name}_delete",
                    "path": f"{menu.path}/delete",
                    "component": "",
                    "title": "删除",
                    "icon": "",
                    "sort": 3,
                    "menu_type": "button",
                    "parent_id": menu.id,
                    "roles": menu.roles,
                    "auth_name": "删除",
                    "auth_mark": "delete",
                    "auth_sort": 3
                }
            ]
            
            # 为特定菜单添加额外的权限按钮
            if menu.name == "Menus":  # 菜单管理
                auth_buttons.append({
                    "name": f"{menu.name}_permission",
                    "path": f"{menu.path}/permission",
                    "component": "",
                    "title": "菜单权限",
                    "icon": "",
                    "sort": 4,
                    "menu_type": "button",
                    "parent_id": menu.id,
                    "roles": menu.roles,
                    "auth_name": "菜单权限",
                    "auth_mark": "permission",
                    "auth_sort": 4
                })
            
            auth_buttons_data.extend(auth_buttons)

        # 插入权限按钮数据
        for auth_button_data in auth_buttons_data:
            auth_button = Menu(**auth_button_data)
            db.add(auth_button)

        # 提交事务
        db.commit()
        print(f"成功初始化 {len(auth_buttons_data)} 条权限按钮数据")

    except Exception as e:
        db.rollback()
        print(f"初始化权限按钮数据失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("开始初始化菜单权限按钮数据...")
    init_menu_auth_buttons()
    print("菜单权限按钮数据初始化完成")
