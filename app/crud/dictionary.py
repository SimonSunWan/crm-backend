from sqlalchemy.orm import Session

from app.core.crud import CRUDBase
from app.models.dictionary import DictionaryEnum, DictionaryType


class CRUDDictionaryType(CRUDBase[DictionaryType]):
    """字典类型 CRUD 操作"""

    def get_by_code(self, db: Session, code: str):
        """根据编码获取字典类型"""
        return db.query(self.model).filter(self.model.code == code).first()

    def get_by_name(self, db: Session, name: str):
        """根据名称获取字典类型"""
        return db.query(self.model).filter(self.model.name == name).first()


class CRUDDictionaryEnum(CRUDBase[DictionaryEnum]):
    """字典枚举 CRUD 操作"""

    def get_by_type_id(
        self, db: Session, type_id: int, skip: int = 0, limit: int = 100
    ):
        """根据类型ID获取字典枚举列表"""
        return (
            db.query(self.model)
            .filter(self.model.type_id == type_id, self.model.status)
            .order_by(self.model.sort_order)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_type_id_and_key(self, db: Session, type_id: int, key_value: str):
        """根据类型ID和键值获取字典枚举"""
        return (
            db.query(self.model)
            .filter(
                self.model.type_id == type_id,
                self.model.key_value == key_value,
                self.model.status,
            )
            .first()
        )

    def get_cascade_by_type_id(self, db: Session, type_id: int):
        """根据类型ID获取级联字典枚举列表"""
        return (
            db.query(self.model)
            .filter(self.model.type_id == type_id, self.model.status)
            .order_by(
                self.model.parent_id.nullsfirst(),
                self.model.level,
                self.model.sort_order,
            )
            .all()
        )

    def get_root_enums(self, db: Session, type_id: int):
        """获取根级枚举（无父级）"""
        return (
            db.query(self.model)
            .filter(
                self.model.type_id == type_id,
                self.model.parent_id.is_(None),
                self.model.status,
            )
            .order_by(self.model.sort_order)
            .all()
        )

    def get_children_by_parent_id(self, db: Session, parent_id: int):
        """根据父级ID获取子级枚举"""
        return (
            db.query(self.model)
            .filter(self.model.parent_id == parent_id, self.model.status)
            .order_by(self.model.sort_order)
            .all()
        )

    def build_cascade_tree(self, db: Session, type_id: int):
        """构建级联树结构"""
        all_enums = self.get_cascade_by_type_id(db, type_id)
        enum_map = {enum.id: enum for enum in all_enums}

        tree = []
        for enum in all_enums:
            enum.children = []
            enum.hasChildren = False

            if enum.parent_id is None:
                tree.append(enum)
            else:
                parent = enum_map.get(enum.parent_id)
                if parent:
                    parent.children.append(enum)
                    parent.hasChildren = True

        return tree

    def delete_by_type_id(self, db: Session, type_id: int):
        """根据类型ID删除所有字典枚举"""
        db.query(self.model).filter(self.model.type_id == type_id).delete()
        db.commit()

    def delete_cascade(self, db: Session, enum_id: int):
        """级联删除字典枚举及其所有子级"""
        # 获取要删除的枚举对象
        enum_obj = self.get_or_404(db, enum_id, "字典枚举未找到")
        
        # 递归删除所有子级
        self._delete_children_recursive(db, enum_id)
        
        # 删除当前枚举
        db.delete(enum_obj)
        db.commit()

    def _delete_children_recursive(self, db: Session, parent_id: int):
        """递归删除所有子级枚举"""
        # 获取所有直接子级
        children = self.get_children_by_parent_id(db, parent_id)
        
        for child in children:
            # 递归删除子级的子级
            self._delete_children_recursive(db, child.id)
            # 删除当前子级
            db.delete(child)


dictionary_type_crud = CRUDDictionaryType(DictionaryType)
dictionary_enum_crud = CRUDDictionaryEnum(DictionaryEnum)
