from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class TimestampMixin:
    """时间戳混入类，提供 created_at 和 updated_at 字段"""
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
