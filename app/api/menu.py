from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_superuser
from app.crud.menu import menu_crud
from app.models.user import User
from app.schemas.base import ApiResponse
from app.schemas.menu import MenuCreate, MenuResponse, MenuUpdate

router = APIRouter()


def menu_to_response(menu) -> MenuResponse:
    """将Menu对象转换为MenuResponse对象"""
    roles_data = None
    if menu.roles:
        from app.schemas.menu import RoleResponseForMenu

        roles_data = []
        for role in menu.roles:
            role_dict = {
                "id": role.id,
                "role_name": role.role_name,
                "role_code": role.role_code,
                "description": role.description,
                "status": role.status,
            }
            roles_data.append(RoleResponseForMenu.model_validate(role_dict))

    menu_dict = {
        "id": menu.id,
        "name": menu.name,
        "path": menu.path,
        "icon": menu.icon,
        "sort": menu.sort,
        "is_hide": menu.is_hide,
        "is_keep_alive": menu.is_keep_alive,
        "is_link": menu.is_link,
        "link": menu.link,
        "is_enable": menu.is_enable,
        "menu_type": menu.menu_type,
        "parent_id": menu.parent_id,
        "roles": roles_data,
        "auth_mark": menu.auth_mark,
        "created_by": menu.created_by,
        "updated_by": menu.updated_by,
        "children": [],
    }

    return MenuResponse.model_validate(menu_dict)


@router.get("/", response_model=ApiResponse)
def get_menus(
    name: Optional[str] = None,
    path: Optional[str] = None,
    menu_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """获取菜单列表"""
    try:
        # 获取所有菜单，构建树形结构
        all_menus = db.query(menu_crud.model).all()

        # 构建树形结构
        def build_tree(menus, parent_id=None):
            tree = []
            for menu in menus:
                if menu.parent_id == parent_id:
                    # 递归构建子菜单
                    children = build_tree(menus, menu.id)
                    # 使用辅助函数转换为MenuResponse对象，然后设置children
                    menu_response = menu_to_response(menu)
                    # 创建新的字典并更新children
                    menu_dict = menu_response.model_dump()
                    menu_dict["children"] = children
                    tree.append(MenuResponse.model_validate(menu_dict))
            # 按sort字段从小到大排序
            tree.sort(key=lambda x: x.sort)
            return tree

        # 构建完整的树形结构
        menu_tree = build_tree(all_menus)

        # 应用过滤条件
        if name or path or menu_type:

            def filter_tree(tree, name_filter=None, path_filter=None, type_filter=None):
                filtered = []
                for menu in tree:
                    # 检查当前菜单是否匹配过滤条件
                    matches = True
                    if name_filter and name_filter.lower() not in menu.name.lower():
                        matches = False
                    if (
                        path_filter
                        and path_filter.lower() not in (menu.path or "").lower()
                        and path_filter.lower() not in (menu.link or "").lower()
                    ):
                        matches = False
                    if (
                        type_filter
                        and type_filter.lower() not in (menu.menu_type or "").lower()
                    ):
                        matches = False

                    # 递归过滤子菜单
                    filtered_children = filter_tree(
                        menu.children, name_filter, path_filter, type_filter
                    )

                    # 如果当前菜单匹配或者有匹配的子菜单，则包含
                    if matches or filtered_children:
                        menu.children = filtered_children
                        filtered.append(menu)
                return filtered

            menu_tree = filter_tree(menu_tree, name, path, menu_type)

        # 计算树形结构的总节点数（包括所有子节点）
        def count_tree_nodes(tree):
            count = len(tree)
            for node in tree:
                if node.children:
                    count += count_tree_nodes(node.children)
            return count

        total_nodes = count_tree_nodes(menu_tree)

        # 返回统一格式的响应（保持树形结构）
        response_data = {
            "records": menu_tree,
            "total": total_nodes,
            "current": 1,
            "size": total_nodes,
        }

        return ApiResponse(code=200, message="操作成功", data=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取菜单列表失败: {str(e)}")


@router.get("/tree", response_model=ApiResponse)
def get_menu_tree(db: Session = Depends(get_db)):
    """获取菜单树形结构"""
    try:
        menus = menu_crud.get_all_menus(db)
        # 转换为响应模型，处理children字段
        menu_responses = []
        for menu in menus:
            menu_response = menu_to_response(menu)
            menu_responses.append(menu_response)
        return ApiResponse(code=200, message="操作成功", data=menu_responses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取菜单树失败: {str(e)}")


@router.get("/navigation", response_model=ApiResponse)
def get_navigation_menus(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    """获取导航菜单（用于左侧菜单和动态路由）"""
    try:
        # 根据用户启用的角色获取菜单
        enabled_roles = (
            [role for role in current_user.roles if role.status]
            if current_user.roles
            else []
        )
        user_roles = [role.role_code for role in enabled_roles]
        if not user_roles:
            # 如果没有启用的角色，返回空菜单
            return ApiResponse(code=200, message="操作成功", data=[])

        # 获取所有启用的菜单
        menus = (
            db.query(menu_crud.model)
            .filter(menu_crud.model.is_enable, ~menu_crud.model.is_hide)
            .all()
        )

        # 过滤用户有权限的菜单
        authorized_menu_ids = set()

        # 检查是否为超级管理员
        is_super_admin = "SUPER" in user_roles

        if is_super_admin:
            # 超级管理员可以看到所有启用的菜单
            authorized_menu_ids = {menu.id for menu in menus}
        else:
            # 普通用户根据启用角色权限过滤菜单
            for menu in menus:
                # 检查菜单是否与用户的启用角色关联
                menu_has_permission = False
                for enabled_role in enabled_roles:
                    if menu in enabled_role.menus:
                        menu_has_permission = True
                        break

                if menu_has_permission:
                    authorized_menu_ids.add(menu.id)

        # 构建树形结构，只包含有权限的菜单（排除权限按钮）
        def build_authorized_tree(parent_id=None):
            tree = []
            for menu in menus:
                if (
                    menu.parent_id == parent_id
                    and menu.id in authorized_menu_ids
                    and menu.menu_type != "button"
                ):
                    # 递归构建子菜单
                    children = build_authorized_tree(menu.id)

                    # 获取菜单关联的角色
                    menu_roles = (
                        [role.role_code for role in menu.roles] if menu.roles else []
                    )

                    # 获取菜单的权限按钮列表
                    auth_list = []
                    if menu.menu_type == "menu":
                        # 查找该菜单下的权限按钮
                        auth_buttons = (
                            db.query(menu_crud.model)
                            .filter(
                                menu_crud.model.parent_id == menu.id,
                                menu_crud.model.menu_type == "button",
                                menu_crud.model.is_enable,
                            )
                            .all()
                        )

                        # 检查当前用户启用角色是否拥有这些按钮的权限
                        for auth_button in auth_buttons:
                            # 检查权限按钮是否与用户启用角色关联
                            button_has_permission = False
                            if is_super_admin:
                                # 超级管理员拥有所有权限
                                button_has_permission = True
                            else:
                                # 检查普通用户启用角色是否拥有该按钮权限
                                for enabled_role in enabled_roles:
                                    if auth_button in enabled_role.menus:
                                        button_has_permission = True
                                        break

                            # 只有拥有权限的按钮才添加到authList中
                            if button_has_permission:
                                auth_list.append(
                                    {
                                        "title": auth_button.name,
                                        "authMark": auth_button.auth_mark,
                                    }
                                )

                    # 转换为字典格式
                    menu_dict = {
                        "id": menu.id,
                        "name": menu.name,
                        "path": menu.path,
                        "meta": {
                            "title": menu.name,
                            "icon": menu.icon,
                            "sort": menu.sort,
                            "isHide": menu.is_hide,
                            "keepAlive": menu.is_keep_alive,
                            "isLink": menu.is_link,
                            "link": menu.link,
                            "isEnable": menu.is_enable,
                            "roles": menu_roles,
                            "authList": auth_list,
                        },
                        "children": children,
                    }
                    tree.append(menu_dict)
            # 按sort字段从小到大排序
            tree.sort(key=lambda x: x["meta"]["sort"])
            return tree

        frontend_menus = build_authorized_tree()

        return ApiResponse(code=200, message="操作成功", data=frontend_menus)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取导航菜单失败: {str(e)}")


@router.post("/", response_model=ApiResponse)
def create_menu(
    menu: MenuCreate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """创建菜单"""
    try:
        # 检查菜单名称是否已存在（同层级查重）
        if menu_crud.get_by_name_and_parent(db, menu.name, menu.parent_id):
            raise HTTPException(status_code=400, detail="菜单名称已存在")

        # 检查权限标识是否已存在（同层级查重，如果提供了权限标识）
        if menu.auth_mark and menu_crud.get_by_auth_mark_and_parent(
            db, menu.auth_mark, menu.parent_id
        ):
            raise HTTPException(status_code=400, detail="权限标识已存在")

        # 检查路径是否已存在（如果提供了路径）
        if menu.path and menu_crud.get_by_path(db, menu.path):
            raise HTTPException(status_code=400, detail="路由路径已存在")

        # 创建菜单数据
        menu_data = menu.model_dump()
        menu_data["created_by"] = current_user.user_name

        # 如果有parent_id，验证父菜单是否存在
        if menu.parent_id:
            menu_crud.get_or_404(db, menu.parent_id, "父菜单不存在")

        created_menu = menu_crud.create(db, menu_data)

        # 更新父菜单的is_enable状态
        menu_crud.update_parent_enable_status(db, created_menu.id)

        # 转换为响应模型，处理children字段
        menu_response = menu_to_response(created_menu)

        return ApiResponse(code=200, message="菜单创建成功", data=menu_response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建菜单失败: {str(e)}")


@router.get("/{menu_id}", response_model=ApiResponse)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    """获取单个菜单"""
    try:
        menu = menu_crud.get_or_404(db, menu_id, "菜单未找到")
        # 转换为响应模型，处理children字段
        menu_response = menu_to_response(menu)
        return ApiResponse(code=200, message="操作成功", data=menu_response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取菜单失败: {str(e)}")


@router.put("/{menu_id}", response_model=ApiResponse)
def update_menu(
    menu_id: int,
    menu: MenuUpdate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """更新菜单"""
    try:
        # 检查菜单是否存在
        existing_menu = menu_crud.get_or_404(db, menu_id, "菜单未找到")

        # 检查名称是否重复（如果更新了名称，同层级查重）
        if menu.name and menu.name != existing_menu.name:
            if menu_crud.get_by_name_and_parent(db, menu.name, existing_menu.parent_id):
                raise HTTPException(status_code=400, detail="菜单名称已存在")

        # 检查权限标识是否重复（如果更新了权限标识，同层级查重）
        if menu.auth_mark and menu.auth_mark != existing_menu.auth_mark:
            if menu_crud.get_by_auth_mark_and_parent(
                db, menu.auth_mark, existing_menu.parent_id
            ):
                raise HTTPException(status_code=400, detail="权限标识已存在")

        # 检查路径是否重复（如果更新了路径）
        if menu.path and menu.path != existing_menu.path:
            if menu_crud.get_by_path(db, menu.path):
                raise HTTPException(status_code=400, detail="路由路径已存在")

        # 更新菜单数据
        update_data = menu.model_dump(exclude_unset=True)
        update_data["updated_by"] = current_user.user_name

        updated_menu = menu_crud.update(db, existing_menu, update_data)

        # 更新父菜单的is_enable状态
        menu_crud.update_parent_enable_status(db, menu_id)

        # 转换为响应模型，处理children字段
        menu_response = menu_to_response(updated_menu)
        return ApiResponse(code=200, message="菜单更新成功", data=menu_response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新菜单失败: {str(e)}")


@router.delete("/{menu_id}", response_model=ApiResponse)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """删除菜单"""
    try:
        # 检查菜单是否存在
        menu = menu_crud.get_or_404(db, menu_id, "菜单未找到")

        # 检查是否有子菜单
        children_count = (
            db.query(menu_crud.model)
            .filter(menu_crud.model.parent_id == menu_id)
            .count()
        )
        if children_count > 0:
            raise HTTPException(
                status_code=400,
                detail=f"该菜单下有 {children_count} 个子菜单，无法删除",
            )

        # 在删除菜单之前，清理相关角色的权限
        from app.models.role import Role
        from app.models.role_menu import role_menu

        # 查找所有关联了该菜单的角色
        roles_with_menu = (
            db.query(Role).join(role_menu).filter(role_menu.c.menu_id == menu_id).all()
        )

        # 从这些角色中移除该菜单的权限
        for role in roles_with_menu:
            role.menus = [m for m in role.menus if m.id != menu_id]

        # 保存父菜单ID用于后续更新
        parent_id = menu.parent_id

        # 删除菜单
        menu_crud.delete(db, menu)

        # 提交事务
        db.commit()

        # 更新父菜单的is_enable状态
        if parent_id:
            menu_crud.update_parent_enable_status(db, parent_id)

        return ApiResponse(code=200, message="菜单删除成功")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除菜单失败: {str(e)}")
