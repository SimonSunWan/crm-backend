from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.user_role import user_role


class User(Base, TimestampMixin):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    create_by = Column(String, nullable=True)
    create_time = Column(DateTime, nullable=True)
    update_by = Column(String, nullable=True)
    update_time = Column(DateTime, nullable=True)
    status = Column(String, nullable=True)
    user_name = Column(String, unique=True, index=True, nullable=False)
    nick_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    avatar = Column(String, nullable=True)  # 头像URL
    hashed_password = Column(String, nullable=False)
    
    # 与角色的多对多关系
    roles = relationship("Role", secondary=user_role, back_populates="users")
