from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Department(Base, TimestampMixin):
    """部门模型"""

    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    dept_name = Column(String(100), nullable=False, comment="部门名称")
    parent_id = Column(Integer, ForeignKey("department.id"), nullable=True, comment="父部门ID")
    level = Column(Integer, default=1, comment="部门层级")
    path = Column(String(500), nullable=True, comment="部门路径")
    sort_order = Column(Integer, default=0, comment="排序")
    status = Column(Boolean, default=True, comment="启用状态")

    # 关系
    parent = relationship("Department", backref="children", remote_side=[id])
    users = relationship("User", secondary="user_department", back_populates="departments")
    leaders = relationship("User", secondary="department_leader", back_populates="leading_departments")


class UserDepartment(Base):
    """用户部门关联表"""

    __tablename__ = "user_department"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    dept_id = Column(Integer, ForeignKey("department.id"), primary_key=True)
    join_date = Column(String(20), nullable=True, comment="加入部门日期")
    is_active = Column(Boolean, default=True, comment="是否在职")


class DepartmentLeader(Base):
    """部门负责人关联表"""

    __tablename__ = "department_leader"

    dept_id = Column(Integer, ForeignKey("department.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    is_primary = Column(Boolean, default=False, comment="是否为主要负责人")
