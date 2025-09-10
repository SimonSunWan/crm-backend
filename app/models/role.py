from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.role_menu import role_menu
from app.models.user_role import user_role


class Role(Base, TimestampMixin):
    """角色模型"""

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(
        String(50), unique=True, index=True, nullable=False, comment="角色名称"
    )
    role_code = Column(
        String(50), unique=True, index=True, nullable=False, comment="角色编码"
    )
    description = Column(Text, nullable=True, comment="角色描述")
    status = Column(Boolean, default=True, comment="启用状态")

    # 与用户的多对多关系
    users = relationship("User", secondary=user_role, back_populates="roles")

    # 与菜单的多对多关系
    menus = relationship("Menu", secondary=role_menu, back_populates="roles")
