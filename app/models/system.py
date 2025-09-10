from sqlalchemy import Boolean, Column, Integer, String

from app.core.database import Base
from app.models.base import TimestampMixin


class SystemSetting(Base, TimestampMixin):
    """系统配置表"""

    __tablename__ = "system_setting"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Boolean, default=True)
    setting_key = Column(
        String, unique=True, index=True, nullable=False, comment="配置键"
    )
    setting_value = Column(String, nullable=False, comment="配置值")
    setting_name = Column(String, nullable=False, comment="配置名称")
    setting_desc = Column(String, nullable=True, comment="配置描述")
