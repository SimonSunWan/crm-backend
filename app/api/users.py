from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.base import ApiResponse
from app.crud.user import user_crud
from app.models.user import User

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


@router.get("/me", response_model=ApiResponse)
def get_current_user_info(current_user: User = Depends(get_current_user_dependency)):
    """获取当前登录用户的个人信息"""
    try:
        return ApiResponse(data=UserResponse.model_validate(current_user))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户信息失败: {str(e)}")


@router.get("/", response_model=ApiResponse)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取用户列表"""
    try:
        users = user_crud.get_multi(db, skip=skip, limit=limit)
        return ApiResponse(data=users)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户列表失败: {str(e)}")


@router.post("/", response_model=ApiResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """创建用户"""
    try:
        created_user = user_crud.create(db, user.model_dump())
        return ApiResponse(message="用户创建成功", data=created_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建用户失败: {str(e)}")


@router.get("/{user_id}", response_model=ApiResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """获取单个用户"""
    try:
        user = user_crud.get_or_404(db, user_id, "用户未找到")
        return ApiResponse(data=user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户失败: {str(e)}")


@router.put("/{user_id}", response_model=ApiResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """更新用户"""
    try:
        user = user_crud.get_or_404(db, user_id, "用户未找到")
        updated_user = user_crud.update(db, user, user_update.model_dump(exclude_unset=True))
        return ApiResponse(message="用户更新成功", data=updated_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新用户失败: {str(e)}")


@router.delete("/{user_id}", response_model=ApiResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """删除用户"""
    try:
        user = user_crud.get_or_404(db, user_id, "用户未找到")
        user_crud.delete(db, user)
        return ApiResponse(message="用户删除成功")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除用户失败: {str(e)}")
