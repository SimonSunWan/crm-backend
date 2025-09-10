from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_superuser
from app.core.exceptions import CRMException
from app.core.messages import Messages, success_response
from app.crud.system import system_setting_crud
from app.models.user import User
from app.schemas.base import ApiResponse
from app.schemas.system import SystemSettingResponse

router = APIRouter()


@router.get("/{setting_key}", response_model=ApiResponse)
def get_system_setting(
    setting_key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    """根据键获取系统配置（需要超级管理员权限）"""
    setting = system_setting_crud.get_by_key(db, setting_key=setting_key)
    if not setting:
        raise CRMException(status_code=404, detail="系统配置不存在")

    setting_data = SystemSettingResponse.model_validate(setting)
    return success_response(message=Messages.SYSTEM_CONFIG_SUCCESS, data=setting_data)
