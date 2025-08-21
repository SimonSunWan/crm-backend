from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.schemas.base import ApiResponse
from app.crud.role import role_crud
from app.models.user import User
from app.models.menu import Menu

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
    role_name: str = None,
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
        users_with_role = db.query(User).filter(User.roles.any(role.role_code)).first()
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
        
        # 获取角色关联的菜单ID列表（包括权限按钮）
        menu_ids = []
        for menu in role.menus:
            menu_ids.append(menu.id)
            # 如果菜单有权限按钮，也添加权限按钮的ID（使用前端期望的格式）
            if menu.menu_type == "menu":
                auth_buttons = db.query(Menu).filter(
                    Menu.parent_id == menu.id,
                    Menu.menu_type == "button"
                ).all()
                for auth_button in auth_buttons:
                    # 使用前端期望的格式：menuId_authMark
                    auth_id = f"{menu.id}_{auth_button.auth_mark}"
                    menu_ids.append(auth_id)
        
        return ApiResponse(data={"menuIds": menu_ids})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取角色菜单权限失败: {str(e)}")


@router.post("/{role_id}/menus", response_model=ApiResponse)
def update_role_menus(
    role_id: int,
    menu_data: dict,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """更新角色的菜单权限"""
    try:
        role = role_crud.get_or_404(db, role_id, "角色未找到")
        
        # 从请求数据中获取菜单ID列表
        menu_ids = menu_data.get("menu_ids", [])
        
        # 处理菜单ID列表，包括权限按钮的ID映射
        processed_menu_ids = []
        for menu_id in menu_ids:
            if isinstance(menu_id, str) and '_' in menu_id:
                # 处理权限按钮ID格式：menuId_authMark
                menu_id_str, auth_mark = menu_id.split('_', 1)
                try:
                    parent_menu_id = int(menu_id_str)
                    # 查找对应的权限按钮
                    auth_button = db.query(Menu).filter(
                        Menu.parent_id == parent_menu_id,
                        Menu.menu_type == "button",
                        Menu.auth_mark == auth_mark
                    ).first()
                    if auth_button:
                        processed_menu_ids.append(auth_button.id)
                except ValueError:
                    continue
            else:
                # 直接添加菜单ID
                processed_menu_ids.append(menu_id)
        
        # 获取所有菜单和权限按钮
        menus = db.query(Menu).filter(Menu.id.in_(processed_menu_ids)).all()
        
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
