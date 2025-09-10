from app.core.crud import CRUDBase
from app.models.role import Role


class CRUDRole(CRUDBase[Role]):
    """角色 CRUD 操作"""

    def get_by_code(self, db, role_code: str):
        """根据角色编码获取角色"""
        return db.query(self.model).filter(self.model.role_code == role_code).first()

    def get_by_name(self, db, role_name: str):
        """根据角色名称获取角色"""
        return db.query(self.model).filter(self.model.role_name == role_name).first()


role_crud = CRUDRole(Role)
