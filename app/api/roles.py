from fastapi import APIRouter, Depends, HTTPException, Header, Body, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.schemas.base import ApiResponse
from app.crud.role import role_crud
from app.models.user import User
from app.models.menu import Menu
from app.models.role import Role

router = APIRouter()


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
def get_roles(
    current: int = 1, 
    size: int = 100, 
    role_name: str = Query(None, alias="roleName"),
    db: Session = Depends(get_db)
):
    """获取角色列表"""
    try:
        skip = (current - 1) * size
        
        # 构建查询，过滤掉超级管理员角色
        query = db.query(role_crud.model).filter(role_crud.model.role_code != "SUPER")
        
        # 如果提供了角色名称，添加过滤条件
        if role_name:
            query = query.filter(role_crud.model.role_name.contains(role_name))
        
        # 获取总数
        total = query.count()
        
        # 获取分页数据
        roles = query.offset(skip).limit(size).all()
        
        # 转换为响应模型
        role_responses = [RoleResponse.model_validate(role) for role in roles]
        # 返回包含分页信息的响应
        response_data = {
            "records": role_responses,
            "total": total,
            "current": current,
            "size": size
        }
        
        return ApiResponse(data=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取角色列表失败: {str(e)}")


@router.get("/all", response_model=ApiResponse)
def get_all_roles(db: Session = Depends(get_db)):
    """获取所有角色（不分页）"""
    try:
        # 获取所有启用的角色，过滤掉超级管理员
        roles = db.query(role_crud.model).filter(
            role_crud.model.status == True,
            role_crud.model.role_code != "SUPER"
        ).all()
        
        # 转换为响应模型
        role_responses = [RoleResponse.model_validate(role) for role in roles]
        
        return ApiResponse(data=role_responses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取所有角色失败: {str(e)}")


@router.post("/", response_model=ApiResponse)
def create_role(
    role: RoleCreate, 
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """创建角色"""
    try:
        # 检查角色名称是否已存在
        if role_crud.get_by_name(db, role.role_name):
            raise HTTPException(status_code=400, detail="角色名称已存在")
        
        # 检查角色编码是否已存在
        if role_crud.get_by_code(db, role.role_code):
            raise HTTPException(status_code=400, detail="角色编码已存在")
        
        # 创建角色数据
        role_data = role.model_dump()
        role_data["create_by"] = current_user.user_name
        
        created_role = role_crud.create(db, role_data)
        return ApiResponse(message="角色创建成功", data=RoleResponse.model_validate(created_role))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建角色失败: {str(e)}")


@router.get("/{role_id}", response_model=ApiResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    """获取单个角色"""
    try:
        role = role_crud.get_or_404(db, role_id, "角色未找到")
        return ApiResponse(data=RoleResponse.model_validate(role))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取角色失败: {str(e)}")


@router.put("/{role_id}", response_model=ApiResponse)
def update_role(
    role_id: int, 
    role_update: RoleUpdate, 
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """更新角色"""
    try:
        role = role_crud.get_or_404(db, role_id, "角色未找到")
        
        # 检查更新的角色名称是否与其他角色冲突
        if role_update.role_name and role_update.role_name != role.role_name:
            existing_role = role_crud.get_by_name(db, role_update.role_name)
            if existing_role and existing_role.id != role_id:
                raise HTTPException(status_code=400, detail="角色名称已存在")
        
        # 检查更新的角色编码是否与其他角色冲突
        if role_update.role_code and role_update.role_code != role.role_code:
            existing_role = role_crud.get_by_code(db, role_update.role_code)
            if existing_role and existing_role.id != role_id:
                raise HTTPException(status_code=400, detail="角色编码已存在")
        
        # 更新角色数据
        update_data = role_update.model_dump(exclude_unset=True)
        update_data["update_by"] = current_user.user_name
        
        updated_role = role_crud.update(db, role, update_data)
        return ApiResponse(message="角色更新成功", data=RoleResponse.model_validate(updated_role))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新角色失败: {str(e)}")


@router.delete("/{role_id}", response_model=ApiResponse)
def delete_role(
    role_id: int, 
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """删除角色"""
    try:
        role = role_crud.get_or_404(db, role_id, "角色未找到")
        
        # 检查是否有用户使用该角色
        from app.models.user import User
        users_with_role = db.query(User).filter(User.roles.any(Role.id == role.id)).first()
        if users_with_role:
            raise HTTPException(status_code=400, detail="该角色正在被用户使用，无法删除")
        
        role_crud.delete(db, role)
        return ApiResponse(message="角色删除成功")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除角色失败: {str(e)}")


@router.get("/{role_id}/menus", response_model=ApiResponse)
def get_role_menus(
    role_id: int,
    db: Session = Depends(get_db)
):
    """获取角色的菜单权限"""
    try:
        role = role_crud.get_or_404(db, role_id, "角色未找到")
        
        # 获取所有启用的菜单和权限按钮，按类型和排序分组
        all_menus = db.query(Menu).filter(
            Menu.is_enable == True
        ).order_by(Menu.menu_type, Menu.sort).all()
        
        # 构建菜单树
        def build_menu_tree(menus, parent_id=None):
            tree = []
            for menu in menus:
                if menu.parent_id == parent_id:
                    node = {
                        "id": menu.id,
                        "name": menu.name,
                        "title": menu.title,
                        "path": menu.path,
                        "icon": menu.icon,
                        "sort": menu.sort,
                        "menuType": menu.menu_type,
                        "authName": menu.auth_name,
                        "authMark": menu.auth_mark,
                        "authSort": menu.auth_sort,
                        "isEnable": menu.is_enable,
                        "children": build_menu_tree(menus, menu.id)
                    }
                    tree.append(node)
            return tree
        
        menu_tree = build_menu_tree(all_menus)
        
        # 获取角色已选择的菜单和权限ID
        selected_ids = []
        if role.menus:
            for menu in role.menus:
                # 直接添加菜单或权限按钮的实际ID
                selected_ids.append(menu.id)
        
        return ApiResponse(data={
            "menuTree": menu_tree,
            "selectedIds": selected_ids
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取角色菜单权限失败: {str(e)}")


@router.post("/{role_id}/menus", response_model=ApiResponse)
def update_role_menus(
    role_id: int,
    menu_data: dict = Body(...),
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """更新角色的菜单权限"""
    try:
        role = role_crud.get_or_404(db, role_id, "角色未找到")
        
        # 从请求数据中获取菜单ID列表
        menu_ids = menu_data.get("menuIds", [])
        
        # 如果菜单ID列表为空，直接清空角色权限并返回
        if not menu_ids:
            role.menus.clear()
            db.commit()
            return ApiResponse(message="角色菜单权限已清空")
        
        # 获取所有菜单和权限按钮，只获取启用的菜单
        menus = db.query(Menu).filter(
            Menu.id.in_(menu_ids),
            Menu.is_enable == True  # 只获取启用的菜单
        ).all()
        
        # 清空当前角色的菜单权限
        role.menus.clear()
        
        # 添加新的菜单权限
        role.menus.extend(menus)
        
        db.commit()
        return ApiResponse(message="角色菜单权限更新成功")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新角色菜单权限失败: {str(e)}")


@router.post("/cleanup-orphaned-permissions", response_model=ApiResponse)
def cleanup_orphaned_permissions(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """清理所有角色中已删除菜单的权限"""
    try:
        from app.models.role import Role
        
        # 获取所有角色
        roles = db.query(Role).all()
        cleaned_count = 0
        
        for role in roles:
            # 过滤掉已删除的菜单
            valid_menus = []
            for menu in role.menus:
                # 检查菜单是否仍然存在于数据库中且是启用的
                existing_menu = db.query(Menu).filter(
                    Menu.id == menu.id,
                    Menu.is_enable == True
                ).first()
                
                if existing_menu:
                    valid_menus.append(menu)
                else:
                    cleaned_count += 1
            
            # 更新角色的菜单权限
            if len(valid_menus) != len(role.menus):
                role.menus = valid_menus
        
        db.commit()
        
        return ApiResponse(
            message=f"权限清理完成，共清理了 {cleaned_count} 个无效权限",
            data={"cleanedCount": cleaned_count}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"清理无效权限失败: {str(e)}")
