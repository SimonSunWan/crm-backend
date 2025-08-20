from sqlalchemy import Column, Integer, String, Boolean, ARRAY, DateTime
from app.core.database import Base
from app.models.base import TimestampMixin


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
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    roles = Column(ARRAY(String), nullable=True)
