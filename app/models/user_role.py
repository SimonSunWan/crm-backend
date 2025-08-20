from sqlalchemy import Column, Integer, ForeignKey, Table
from app.core.database import Base

# 用户角色关联表
user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)
