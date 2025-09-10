from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.role_menu import role_menu


class Menu(Base, TimestampMixin):
    """菜单模型"""
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="菜单名称")
    path = Column(String(200), nullable=True, comment="路由地址")
    icon = Column(String(100), nullable=True, comment="菜单图标")
    sort = Column(Integer, default=1, comment="菜单排序")
    is_hide = Column(Boolean, default=False, comment="是否隐藏")
    is_keep_alive = Column(Boolean, default=True, comment="是否缓存")
    is_link = Column(Boolean, default=False, comment="是否外链")
    link = Column(String(500), nullable=True, comment="外部链接")
    is_enable = Column(Boolean, default=True, comment="是否启用")
    menu_type = Column(String(20), default="menu", comment="菜单类型：menu-菜单，button-权限")
    parent_id = Column(Integer, ForeignKey("menus.id"), nullable=True, comment="父菜单ID")
    
    # 权限相关字段
    auth_mark = Column(String(100), nullable=True, comment="权限标识")
    
    # 关系
    children = relationship("Menu", backref="parent", remote_side=[id])
    
    # 与角色的多对多关系
    roles = relationship("Role", secondary=role_menu, back_populates="menus")
