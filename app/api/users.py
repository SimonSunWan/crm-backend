from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.base import ApiResponse
from app.crud.user import user_crud

router = APIRouter()


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
