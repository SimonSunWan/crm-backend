from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func


class TimestampMixin:
    """时间戳混入类，提供 create_time、update_time、created_by 和 updated_by 字段"""

    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String(100), nullable=True, comment="创建者")
    updated_by = Column(String(100), nullable=True, comment="更新者")
