from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.user_role import user_role


class User(Base, TimestampMixin):
    """用户模型"""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Boolean, default=True, nullable=True)
    user_name = Column(String, unique=True, index=True, nullable=False)
    nick_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    avatar = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)

    # 关系
    roles = relationship("Role", secondary=user_role, back_populates="users")
    departments = relationship("Department", secondary="user_department", back_populates="users")
    leading_departments = relationship("Department", secondary="department_leader", back_populates="leaders")