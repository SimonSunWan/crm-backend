from app.core.crud import CRUDBase
from app.models.menu import Menu
from sqlalchemy.orm import Session
from typing import List, Optional


class CRUDMenu(CRUDBase[Menu]):
    """菜单 CRUD 操作"""
    
    def get_by_name(self, db: Session, name: str) -> Optional[Menu]:
        """根据菜单名称获取菜单"""
        return db.query(self.model).filter(self.model.name == name).first()
    
    def get_by_path(self, db: Session, path: str) -> Optional[Menu]:
        """根据路径获取菜单"""
        return db.query(self.model).filter(self.model.path == path).first()
    
    def get_tree(self, db: Session, parent_id: Optional[int] = None) -> List[Menu]:
        """获取菜单树形结构"""
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


menu_crud = CRUDMenu(Menu)
