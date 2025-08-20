from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.menu import MenuCreate, MenuResponse, MenuUpdate
from app.schemas.base import ApiResponse
from app.crud.menu import menu_crud
from app.models.user import User
from typing import Optional

router = APIRouter()


def menu_to_response(menu) -> dict:
    """将Menu对象转换为MenuResponse字典，避免children字段验证问题"""
    return {
        "id": menu.id,
        "name": menu.name,
        "path": menu.path,
        "component": menu.component,
        "redirect": menu.redirect,
        "title": menu.title,
        "icon": menu.icon,
        "sort": menu.sort,
        "is_hide": menu.is_hide,
        "is_keep_alive": menu.is_keep_alive,
        "is_iframe": menu.is_iframe,
        "link": menu.link,
        "is_enable": menu.is_enable,
        "menu_type": menu.menu_type,
        "parent_id": menu.parent_id,
        "roles": menu.roles,
        "auth_name": menu.auth_name,
        "auth_mark": menu.auth_mark,
        "auth_sort": menu.auth_sort,
        "create_by": menu.create_by,
        "create_time": menu.create_time,
        "update_by": menu.update_by,
        "update_time": menu.update_time,
        "children": []
    }


def get_current_user_dependency(authorization: str = Header(...), db: Session = Depends(get_db)) -> User:
    """获取当前登录用户的依赖函数"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="无效的认证头")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="无效的token或用户不存在")
    if not user.status:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    return user


@router.get("/", response_model=ApiResponse)
def get_menus(
    current: int = 1, 
    size: int = 100, 
    name: Optional[str] = None,
    path: Optional[str] = None,
    menu_type: Optional[str] = None,
    db: Session = Depends(get_db)
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
                    # 使用辅助函数转换为字典，然后设置children
                    menu_dict = menu_to_response(menu)
                    menu_dict["children"] = children
                    menu_response = MenuResponse.model_validate(menu_dict)
                    tree.append(menu_response)
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
                    if name_filter and name_filter.lower() not in menu.title.lower():
                        matches = False
                    if path_filter and path_filter.lower() not in (menu.path or "").lower():
                        matches = False
                    if type_filter and type_filter.lower() not in (menu.menu_type or "").lower():
                        matches = False
                    
                    # 递归过滤子菜单
                    filtered_children = filter_tree(menu.children, name_filter, path_filter, type_filter)
                    
                    # 如果当前菜单匹配或者有匹配的子菜单，则包含
                    if matches or filtered_children:
                        menu.children = filtered_children
                        filtered.append(menu)
                return filtered
            
            menu_tree = filter_tree(menu_tree, name, path, menu_type)
        
        # 计算总数（包括所有层级的菜单）
        def count_total(tree):
            total = 0
            for menu in tree:
                total += 1
                total += count_total(menu.children)
            return total
        
        total_count = count_total(menu_tree)
        
        # 返回树形结构数据
        response_data = {
            "records": menu_tree,
            "total": total_count,
            "current": current,
            "size": size
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
            menu_dict = menu_to_response(menu)
            menu_response = MenuResponse.model_validate(menu_dict)
            menu_responses.append(menu_response)
        return ApiResponse(code=200, message="操作成功", data=menu_responses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取菜单树失败: {str(e)}")


@router.get("/navigation", response_model=ApiResponse)
def get_navigation_menus(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """获取导航菜单（用于左侧菜单和动态路由）"""
    try:
        # 根据用户角色获取菜单
        user_roles = current_user.roles or []
        if not user_roles:
            # 如果没有角色，返回空菜单
            return ApiResponse(code=200, message="操作成功", data=[])
        
        # 获取所有启用的菜单
        menus = db.query(menu_crud.model).filter(
            menu_crud.model.is_enable == True,
            menu_crud.model.is_hide == False
        ).all()
        
        # 过滤用户有权限的菜单
        authorized_menu_ids = set()
        for menu in menus:
            if not menu.roles:
                # 如果没有设置角色限制，则所有用户都可以访问
                authorized_menu_ids.add(menu.id)
            else:
                # 处理菜单的角色权限（支持多种格式）
                menu_roles = []
                try:
                    import json
                    # 尝试解析为JSON数组
                    parsed_roles = json.loads(menu.roles)
                    if isinstance(parsed_roles, list):
                        menu_roles = parsed_roles
                    else:
                        menu_roles = [str(parsed_roles)]
                except (json.JSONDecodeError, TypeError):
                    # 如果不是JSON，按逗号分隔处理
                    menu_roles = [role.strip() for role in menu.roles.split(',') if role.strip()]
                
                # 检查用户角色是否与菜单角色有交集
                if any(role in user_roles for role in menu_roles):
                    authorized_menu_ids.add(menu.id)
        
        # 构建树形结构，只包含有权限的菜单
        def build_authorized_tree(parent_id=None):
            tree = []
            for menu in menus:
                if menu.parent_id == parent_id and menu.id in authorized_menu_ids:
                    # 递归构建子菜单
                    children = build_authorized_tree(menu.id)
                    
                    # 解析菜单角色
                    menu_roles = []
                    if menu.roles:
                        try:
                            import json
                            # 尝试解析为JSON数组
                            parsed_roles = json.loads(menu.roles)
                            if isinstance(parsed_roles, list):
                                menu_roles = parsed_roles
                            else:
                                menu_roles = [str(parsed_roles)]
                        except (json.JSONDecodeError, TypeError):
                            # 如果不是JSON，按逗号分隔处理
                            menu_roles = [role.strip() for role in menu.roles.split(',') if role.strip()]
                    
                    # 转换为字典格式
                    menu_dict = {
                        "id": menu.id,
                        "name": menu.name,
                        "path": menu.path,
                        "component": menu.component,
                        "redirect": menu.redirect,
                        "meta": {
                            "title": menu.title,
                            "icon": menu.icon,
                            "sort": menu.sort,
                            "isHide": menu.is_hide,
                            "keepAlive": menu.is_keep_alive,
                            "isIframe": menu.is_iframe,
                            "link": menu.link,
                            "isEnable": menu.is_enable,
                            "roles": menu_roles,  # 使用已经解析的角色列表
                            "authList": []  # 权限列表需要单独处理
                        },
                        "children": children
                    }
                    tree.append(menu_dict)
            return tree
        
        frontend_menus = build_authorized_tree()
        
        return ApiResponse(code=200, message="操作成功", data=frontend_menus)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取导航菜单失败: {str(e)}")


@router.post("/", response_model=ApiResponse)
def create_menu(
    menu: MenuCreate, 
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """创建菜单"""
    try:
        print(f"创建菜单 - 接收到的数据: {menu}")
        
        # 检查菜单名称是否已存在
        if menu_crud.get_by_name(db, menu.name):
            raise HTTPException(status_code=400, detail="菜单名称已存在")
        
        # 检查路径是否已存在（如果提供了路径）
        if menu.path and menu_crud.get_by_path(db, menu.path):
            raise HTTPException(status_code=400, detail="路由路径已存在")
        
        # 创建菜单数据
        menu_data = menu.model_dump()
        menu_data["create_by"] = current_user.user_name
        
        print(f"创建菜单 - 处理后的数据: {menu_data}")
        
        # 如果有parent_id，验证父菜单是否存在
        if menu.parent_id:
            parent_menu = menu_crud.get_or_404(db, menu.parent_id, "父菜单不存在")
        
        created_menu = menu_crud.create(db, menu_data)
        
        # 转换为响应模型，处理children字段
        menu_dict = menu_to_response(created_menu)
        menu_response = MenuResponse.model_validate(menu_dict)
        
        return ApiResponse(code=200, message="菜单创建成功", data=menu_response)
    except HTTPException:
        raise
    except Exception as e:
        print(f"创建菜单 - 错误详情: {str(e)}")
        import traceback
        print(f"创建菜单 - 错误堆栈: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"创建菜单失败: {str(e)}")


@router.get("/{menu_id}", response_model=ApiResponse)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    """获取单个菜单"""
    try:
        menu = menu_crud.get_or_404(db, menu_id, "菜单未找到")
        # 转换为响应模型，处理children字段
        menu_dict = menu_to_response(menu)
        menu_response = MenuResponse.model_validate(menu_dict)
        return ApiResponse(code=200, message="操作成功", data=menu_response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取菜单失败: {str(e)}")


@router.put("/{menu_id}", response_model=ApiResponse)
def update_menu(
    menu_id: int,
    menu: MenuUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """更新菜单"""
    try:
        # 检查菜单是否存在
        existing_menu = menu_crud.get_or_404(db, menu_id, "菜单未找到")
        
        # 检查名称是否重复（如果更新了名称）
        if menu.name and menu.name != existing_menu.name:
            if menu_crud.get_by_name(db, menu.name):
                raise HTTPException(status_code=400, detail="菜单名称已存在")
        
        # 检查路径是否重复（如果更新了路径）
        if menu.path and menu.path != existing_menu.path:
            if menu_crud.get_by_path(db, menu.path):
                raise HTTPException(status_code=400, detail="路由路径已存在")
        
        # 更新菜单数据
        update_data = menu.model_dump(exclude_unset=True)
        update_data["update_by"] = current_user.user_name
        
        updated_menu = menu_crud.update(db, existing_menu, update_data)
        # 转换为响应模型，处理children字段
        menu_dict = menu_to_response(updated_menu)
        menu_response = MenuResponse.model_validate(menu_dict)
        return ApiResponse(code=200, message="菜单更新成功", data=menu_response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新菜单失败: {str(e)}")


@router.delete("/{menu_id}", response_model=ApiResponse)
def delete_menu(
    menu_id: int,
    db: Session = Depends(get_db)
):
    """删除菜单"""
    try:
        # 检查菜单是否存在
        menu = menu_crud.get_or_404(db, menu_id, "菜单未找到")
        
        # 检查是否有子菜单
        children_count = db.query(menu_crud.model).filter(menu_crud.model.parent_id == menu_id).count()
        if children_count > 0:
            raise HTTPException(status_code=400, detail=f"该菜单下有 {children_count} 个子菜单，无法删除")
        
        # 删除菜单
        menu_crud.delete(db, menu)
        return ApiResponse(code=200, message="菜单删除成功")
    except HTTPException:
        raise
    except Exception as e:
        print(f"删除菜单错误详情: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除菜单失败: {str(e)}")
