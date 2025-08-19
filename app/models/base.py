from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class TimestampMixin:
    """时间戳混入类，提供 create_time 和 update_time 字段"""
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), onupdate=func.now())
