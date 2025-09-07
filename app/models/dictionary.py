from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class DictionaryType(Base, TimestampMixin):
    """字典类型表"""
    __tablename__ = "dic_types"

    id = Column(Integer, primary_key=True, index=True)
    create_by = Column(String, nullable=True)
    create_time = Column(DateTime, nullable=True)
    update_by = Column(String, nullable=True)
    update_time = Column(DateTime, nullable=True)
    status = Column(Boolean, default=True)
    name = Column(String, unique=True, index=True, nullable=False, comment="字典类型名称")
    code = Column(String, unique=True, index=True, nullable=False, comment="字典类型编码")
    description = Column(String, nullable=True, comment="字典类型描述")
    
    # 关联字典枚举
    enums = relationship("DictionaryEnum", back_populates="type", cascade="all, delete-orphan")


class DictionaryEnum(Base, TimestampMixin):
    """字典枚举表"""
    __tablename__ = "dic_enums"

    id = Column(Integer, primary_key=True, index=True)
    create_by = Column(String, nullable=True)
    create_time = Column(DateTime, nullable=True)
    update_by = Column(String, nullable=True)
    update_time = Column(DateTime, nullable=True)
    status = Column(Boolean, default=True)
    type_id = Column(Integer, ForeignKey("dic_types.id"), nullable=False, comment="字典类型ID")
    parent_id = Column(Integer, ForeignKey("dic_enums.id"), nullable=True, comment="父级枚举ID")
    key_value = Column(String, nullable=False, comment="键值")
    dict_value = Column(String, nullable=False, comment="字典值")
    sort_order = Column(Integer, default=0, comment="排序")
    level = Column(Integer, default=1, comment="层级")
    path = Column(String, nullable=True, comment="路径")
    
    # 关联字典类型
    type = relationship("DictionaryType", back_populates="enums")
    
    # 级联关系
    parent = relationship("DictionaryEnum", remote_side=[id], backref="children")
