from datetime import datetime
from typing import Optional

from app.schemas.base import CamelCaseModel


class SystemSettingBase(CamelCaseModel):
    setting_key: str
    setting_value: str
    setting_name: str
    setting_desc: Optional[str] = None
    status: bool = True


class SystemSettingCreate(SystemSettingBase):
    pass


class SystemSettingUpdate(CamelCaseModel):
    setting_value: Optional[str] = None
    setting_name: Optional[str] = None
    setting_desc: Optional[str] = None
    status: Optional[bool] = None


class SystemSettingResponse(SystemSettingBase):
    id: int
    created_by: Optional[str] = None
    create_time: Optional[datetime] = None
    updated_by: Optional[str] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class SystemSettingValueUpdate(CamelCaseModel):
    setting_value: str
