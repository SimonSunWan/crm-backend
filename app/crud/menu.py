from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.cache_decorators import cached
from app.core.crud import CRUDBase
from app.core.redis_client import cache_key_menu_tree
from app.models.menu import Menu


class CRUDMenu(CRUDBase[Menu]):
    """菜单 CRUD 操作"""

    def get_by_name(self, db: Session, name: str) -> Optional[Menu]:
        """根据菜单名称获取菜单"""
        return db.query(self.model).filter(self.model.name == name).first()

    def get_by_name_and_parent(
        self, db: Session, name: str, parent_id: Optional[int] = None
    ) -> Optional[Menu]:
        """根据菜单名称和父ID获取菜单（同层级查重）"""
        return (
            db.query(self.model)
            .filter(self.model.name == name, self.model.parent_id == parent_id)
            .first()
        )

    def get_by_auth_mark_and_parent(
        self, db: Session, auth_mark: str, parent_id: Optional[int] = None
    ) -> Optional[Menu]:
        """根据权限标识和父ID获取菜单（同层级查重）"""
        return (
            db.query(self.model)
            .filter(
                self.model.auth_mark == auth_mark, self.model.parent_id == parent_id
            )
            .first()
        )

    def get_by_path(self, db: Session, path: str) -> Optional[Menu]:
        """根据路径获取菜单"""
        return db.query(self.model).filter(self.model.path == path).first()

    @cached(
        lambda db, parent_id=None: f"{cache_key_menu_tree()}:{parent_id or 'root'}",
        ttl=7200,
    )
    def get_tree(self, db: Session, parent_id: Optional[int] = None) -> List[Menu]:
        """获取菜单树形结构（带缓存）"""
        query = db.query(self.model).filter(self.model.parent_id == parent_id)
        menus = query.order_by(self.model.sort).all()

        for menu in menus:
            children = self.get_tree(db, menu.id)
            if children:
                menu.children = children

        return menus

    def get_all_menus(self, db: Session) -> List[Menu]:
        """获取所有菜单（树形结构）"""
        return self.get_tree(db)

    def get_menus_by_type(self, db: Session, menu_type: str) -> List[Menu]:
        """根据菜单类型获取菜单"""
        return db.query(self.model).filter(self.model.menu_type == menu_type).all()

    def get_menus_by_role(self, db: Session, role: str) -> List[Menu]:
        """根据角色获取菜单"""
        # 这里需要根据roles字段的JSON内容进行查询
        # 简化实现，实际项目中可能需要更复杂的角色权限逻辑
        return db.query(self.model).filter(self.model.roles.contains(role)).all()

    def update_parent_enable_status(self, db: Session, menu_id: int):
        """根据子菜单的is_enable状态更新父菜单的is_enable状态"""
        # 获取当前菜单
        current_menu = db.query(self.model).filter(self.model.id == menu_id).first()
        if not current_menu or not current_menu.parent_id:
            return

        # 只有menu_type为"menu"的菜单才需要更新父菜单状态
        if current_menu.menu_type != "menu":
            return

        parent_id = current_menu.parent_id

        # 获取所有menu_type为menu的子菜单
        children_menus = (
            db.query(self.model)
            .filter(self.model.parent_id == parent_id, self.model.menu_type == "menu")
            .all()
        )

        # 检查所有子菜单的is_enable状态
        all_children_disabled = all(not child.is_enable for child in children_menus)

        # 更新父菜单的is_enable状态
        parent_menu = db.query(self.model).filter(self.model.id == parent_id).first()
        if parent_menu:
            parent_menu.is_enable = not all_children_disabled
            db.commit()

            # 递归更新更上层的父菜单
            self.update_parent_enable_status(db, parent_id)

    def create(self, db: Session, obj_in: dict) -> Menu:
        """创建菜单"""
        menu = super().create(db, obj_in)
        self._invalidate_menu_cache()
        return menu

    def update(self, db: Session, db_obj: Menu, obj_in: dict) -> Menu:
        """更新菜单"""
        menu = super().update(db, db_obj, obj_in)
        self._invalidate_menu_cache()
        return menu

    def delete(self, db: Session, db_obj: Menu) -> None:
        """删除菜单"""
        super().delete(db, db_obj)
        self._invalidate_menu_cache()

    def _invalidate_menu_cache(self):
        """清除菜单相关缓存"""
        from app.core.redis_client import cache_manager

        # 清除菜单树缓存
        cache_manager.delete_pattern("menu:tree:*")


menu_crud = CRUDMenu(Menu)
