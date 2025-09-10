from typing import Optional
from app.models.user import User
from app.models.menu import Menu


def check_data_permission(user: User, menu_path: str, db) -> Optional[str]:
    """
    检查用户的数据权限
    返回权限标识：'view_self' 或 'view_all' 或 None
    """
    if not user.roles:
        return None
    
    # 获取用户启用的角色
    enabled_roles = [role for role in user.roles if role.status]
    if not enabled_roles:
        return None
    
    # 检查是否为超级管理员
    user_role_codes = [role.role_code for role in enabled_roles]
    if "SUPER" in user_role_codes:
        return "view_all"
    
    # 查找对应的菜单 - 支持多种路径格式
    menu_paths = [menu_path, menu_path.rstrip('/'), f"{menu_path}/"]
    menu = None
    for path in menu_paths:
        menu = db.query(Menu).filter(
            Menu.path == path,
            Menu.is_enable == True
        ).first()
        if menu:
            break
    
    if not menu:
        # 如果找不到菜单，默认返回view_all（向后兼容）
        return "view_all"
    
    # 查找该菜单下的权限按钮
    auth_buttons = db.query(Menu).filter(
        Menu.parent_id == menu.id,
        Menu.menu_type == "button",
        Menu.is_enable == True
    ).all()
    
    # 检查用户是否拥有查看全部权限
    for auth_button in auth_buttons:
        if auth_button.auth_mark == "view_all":
            for enabled_role in enabled_roles:
                if auth_button in enabled_role.menus:
                    return "view_all"
    
    # 检查用户是否拥有查看自己权限
    for auth_button in auth_buttons:
        if auth_button.auth_mark == "view_self":
            for enabled_role in enabled_roles:
                if auth_button in enabled_role.menus:
                    return "view_self"
    
    # 如果没有任何权限按钮，默认返回view_all
    return "view_all"


def apply_data_permission_filter(query, user: User, permission: str):
    """
    根据数据权限应用查询过滤
    """
    if permission == "view_self":
        return query.filter(query.model.created_by == user.id)
    elif permission == "view_all":
        return query
    else:
        # 如果没有权限，返回空查询
        return query.filter(False)
