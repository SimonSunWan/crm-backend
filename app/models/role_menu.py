from sqlalchemy import Column, Integer, ForeignKey, Table
from app.core.database import Base

role_menu = Table(
    'role_menu',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('menu_id', Integer, ForeignKey('menus.id'), primary_key=True)
)
