from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.user_role import user_role


class User(Base, TimestampMixin):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Boolean, default=True, nullable=True)  # 统一为Boolean类型
    user_name = Column(String, unique=True, index=True, nullable=False)
    nick_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    avatar = Column(String, nullable=True)  # 头像URL
    hashed_password = Column(String, nullable=False)

    # 与角色的多对多关系
    roles = relationship("Role", secondary=user_role, back_populates="users")
