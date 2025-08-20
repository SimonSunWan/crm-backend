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
        skip = (current - 1) * size
        
        # 构建查询
        query = db.query(menu_crud.model)
        
        # 添加过滤条件
        if name:
            query = query.filter(menu_crud.model.name.contains(name))
        if path:
            query = query.filter(menu_crud.model.path.contains(path))
        if menu_type:
            query = query.filter(menu_crud.model.menu_type == menu_type)
        
        # 获取总数
        total = query.count()
        
        # 获取分页数据
        menus = query.offset(skip).limit(size).all()
        
        # 转换为响应模型
        menu_responses = [MenuResponse.model_validate(menu) for menu in menus]
        
        # 返回包含分页信息的响应
        response_data = {
            "records": menu_responses,
            "total": total,
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
        menu_responses = [MenuResponse.model_validate(menu) for menu in menus]
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
        authorized_menus = []
        for menu in menus:
            if not menu.roles or any(role in user_roles for role in menu.roles.split(',')):
                authorized_menus.append(menu)
        
        # 构建树形结构
        menu_tree = menu_crud.get_tree(db)
        
        # 转换为前端需要的格式
        def convert_to_frontend_format(menu):
            return {
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
                    "roles": menu.roles.split(',') if menu.roles else [],
                    "authList": []  # 权限列表需要单独处理
                },
                "children": [convert_to_frontend_format(child) for child in menu.children] if menu.children else []
            }
        
        frontend_menus = [convert_to_frontend_format(menu) for menu in menu_tree]
        
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
        # 检查菜单名称是否已存在
        if menu_crud.get_by_name(db, menu.name):
            raise HTTPException(status_code=400, detail="菜单名称已存在")
        
        # 检查路径是否已存在（如果提供了路径）
        if menu.path and menu_crud.get_by_path(db, menu.path):
            raise HTTPException(status_code=400, detail="路由路径已存在")
        
        # 创建菜单数据
        menu_data = menu.model_dump()
        menu_data["create_by"] = current_user.user_name
        
        created_menu = menu_crud.create(db, menu_data)
        return ApiResponse(code=200, message="菜单创建成功", data=MenuResponse.model_validate(created_menu))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建菜单失败: {str(e)}")


@router.get("/{menu_id}", response_model=ApiResponse)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    """获取单个菜单"""
    try:
        menu = menu_crud.get_or_404(db, menu_id, "菜单未找到")
        return ApiResponse(code=200, message="操作成功", data=MenuResponse.model_validate(menu))
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
        
        updated_menu = menu_crud.update(db, menu_id, update_data)
        return ApiResponse(code=200, message="菜单更新成功", data=MenuResponse.model_validate(updated_menu))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新菜单失败: {str(e)}")


@router.delete("/{menu_id}", response_model=ApiResponse)
def delete_menu(
    menu_id: int,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """删除菜单"""
    try:
        # 检查菜单是否存在
        menu = menu_crud.get_or_404(db, menu_id, "菜单未找到")
        
        # 检查是否有子菜单
        if menu.children:
            raise HTTPException(status_code=400, detail="该菜单下有子菜单，无法删除")
        
        # 删除菜单
        menu_crud.delete(db, menu_id)
        return ApiResponse(code=200, message="菜单删除成功")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除菜单失败: {str(e)}")
