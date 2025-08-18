from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base
from app.models.base import TimestampMixin


class Customer(Base, TimestampMixin):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    company = Column(String)
    position = Column(String)
    address = Column(Text)
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
