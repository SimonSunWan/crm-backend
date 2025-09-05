from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud.system_setting import system_setting_crud
from app.schemas.system_setting import SystemSettingResponse
from app.schemas.base import ApiResponse
from app.models.user import User
from app.api.users import get_current_user_dependency

router = APIRouter()


@router.get("/{setting_key}", response_model=ApiResponse)
def get_system_setting(
    setting_key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """根据键获取系统配置"""
    try:
        setting = system_setting_crud.get_by_key(db, setting_key=setting_key)
        if not setting:
            raise HTTPException(status_code=404, detail="系统配置不存在")
        
        # 将SQLAlchemy模型转换为Pydantic模型
        setting_data = SystemSettingResponse.model_validate(setting)
        return ApiResponse(message="获取系统配置成功", data=setting_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取系统配置失败: {str(e)}")
