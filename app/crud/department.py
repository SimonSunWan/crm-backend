from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.cache_decorators import cached
from app.core.crud import CRUDBase
from app.models.department import Department


class CRUDDepartment(CRUDBase[Department]):
    """部门 CRUD 操作"""

    def get_by_name(self, db: Session, name: str) -> Optional[Department]:
        """根据部门名称获取部门"""
        return db.query(self.model).filter(self.model.dept_name == name).first()

    def get_by_name_and_parent(
        self, db: Session, name: str, parent_id: Optional[int] = None
    ) -> Optional[Department]:
        """根据部门名称和父ID获取部门（同层级查重）"""
        return (
            db.query(self.model)
            .filter(self.model.dept_name == name, self.model.parent_id == parent_id)
            .first()
        )


    @cached(
        lambda db, parent_id=None: f"department:tree:{parent_id or 'root'}",
        ttl=7200,
    )
    def get_tree(self, db: Session, parent_id: Optional[int] = None) -> List[Department]:
        """获取部门树形结构（带缓存）"""
        query = db.query(self.model).filter(self.model.parent_id == parent_id)
        departments = query.order_by(self.model.sort_order).all()

        for dept in departments:
            children = self.get_tree(db, dept.id)
            if children:
                dept.children = children

        return departments

    def get_all_departments(self, db: Session) -> List[Department]:
        """获取所有部门（树形结构）"""
        return self.get_tree(db)

    def get_users_by_dept(self, db: Session, dept_id: int) -> List:
        """获取部门下的用户"""
        from app.models.user import User

        return db.query(User).join(User.departments).filter(
            Department.id == dept_id
        ).all()

    def update_parent_status(self, db: Session, dept_id: int):
        """根据子部门的status状态更新父部门的status状态"""
        # 获取当前部门
        current_dept = db.query(self.model).filter(self.model.id == dept_id).first()
        if not current_dept or not current_dept.parent_id:
            return

        parent_id = current_dept.parent_id

        # 获取所有子部门
        children_depts = (
            db.query(self.model)
            .filter(self.model.parent_id == parent_id)
            .all()
        )

        # 检查所有子部门的status状态
        all_children_disabled = all(not child.status for child in children_depts)

        # 更新父部门的status状态
        parent_dept = db.query(self.model).filter(self.model.id == parent_id).first()
        if parent_dept:
            parent_dept.status = not all_children_disabled
            db.commit()

            # 递归更新更上层的父部门
            self.update_parent_status(db, parent_id)

    def create(self, db: Session, obj_in: dict) -> Department:
        """创建部门"""
        # 提取负责人ID列表和成员ID列表
        leader_ids = obj_in.pop('leader_ids', [])
        member_ids = obj_in.pop('member_ids', [])
        
        # 创建部门（不提交事务）
        dept = self.model(**obj_in)
        db.add(dept)
        db.flush()  # 获取ID但不提交
        
        # 添加负责人关联
        if leader_ids:
            self._add_leaders(db, dept.id, leader_ids)
        
        # 添加成员关联
        if member_ids:
            self._add_members(db, dept.id, member_ids)
        
        # 提交所有更改
        db.commit()
        db.refresh(dept)
        
        self._invalidate_department_cache()
        return dept

    def update(self, db: Session, db_obj: Department, obj_in: dict) -> Department:
        """更新部门"""
        # 提取负责人ID列表和成员ID列表
        leader_ids = obj_in.pop('leader_ids', None)
        member_ids = obj_in.pop('member_ids', None)
        
        # 更新部门基本信息（不提交事务）
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        # 更新负责人关联
        if leader_ids is not None:
            self._update_leaders(db, db_obj.id, leader_ids)
        
        # 更新成员关联
        if member_ids is not None:
            self._update_members(db, db_obj.id, member_ids)
        
        # 提交所有更改
        db.commit()
        db.refresh(db_obj)
        
        self._invalidate_department_cache()
        return db_obj

    def delete(self, db: Session, db_obj: Department) -> None:
        """删除部门"""
        super().delete(db, db_obj)
        self._invalidate_department_cache()

    def _add_leaders(self, db: Session, dept_id: int, leader_ids: List[int]):
        """添加部门负责人"""
        from app.models.department import DepartmentLeader
        
        for leader_id in leader_ids:
            leader_relation = DepartmentLeader(
                dept_id=dept_id,
                user_id=leader_id,
                is_primary=False
            )
            db.add(leader_relation)

    def _update_leaders(self, db: Session, dept_id: int, leader_ids: List[int]):
        """更新部门负责人"""
        from app.models.department import DepartmentLeader
        
        # 删除现有负责人关联
        db.query(DepartmentLeader).filter(DepartmentLeader.dept_id == dept_id).delete()
        
        # 添加新的负责人关联
        if leader_ids:
            self._add_leaders(db, dept_id, leader_ids)

    def _add_members(self, db: Session, dept_id: int, member_ids: List[int]):
        """添加部门成员"""
        from app.models.department import UserDepartment
        
        for member_id in member_ids:
            member_relation = UserDepartment(
                dept_id=dept_id,
                user_id=member_id,
                is_active=True
            )
            db.add(member_relation)

    def _update_members(self, db: Session, dept_id: int, member_ids: List[int]):
        """更新部门成员"""
        from app.models.department import UserDepartment
        
        # 删除现有成员关联
        db.query(UserDepartment).filter(UserDepartment.dept_id == dept_id).delete()
        
        # 添加新的成员关联
        if member_ids:
            self._add_members(db, dept_id, member_ids)

    def _invalidate_department_cache(self):
        """清除部门相关缓存"""
        from app.core.redis_client import cache_manager

        # 清除部门树缓存
        cache_manager.delete_pattern("department:tree:*")


department_crud = CRUDDepartment(Department)
