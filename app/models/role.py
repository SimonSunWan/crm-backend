from sqlalchemy import Column, Integer, String, Boolean, Text
from app.core.database import Base
from app.models.base import TimestampMixin


class Role(Base, TimestampMixin):
    """角色模型"""
    
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, index=True, nullable=False, comment="角色名称")
    role_code = Column(String(50), unique=True, index=True, nullable=False, comment="角色编码")
    description = Column(Text, nullable=True, comment="角色描述")
    status = Column(Boolean, default=True, comment="启用状态")
    create_by = Column(String(50), nullable=True, comment="创建人")
    update_by = Column(String(50), nullable=True, comment="更新人")
