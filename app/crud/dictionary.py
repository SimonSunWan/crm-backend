from app.core.crud import CRUDBase
from app.models.dictionary import DictionaryType, DictionaryEnum
from sqlalchemy.orm import Session
from typing import List


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

    def get_by_type_id(self, db: Session, type_id: int, skip: int = 0, limit: int = 100):
        """根据类型ID获取字典枚举列表"""
        return db.query(self.model).filter(
            self.model.type_id == type_id,
            self.model.status == True
        ).order_by(self.model.sort_order).offset(skip).limit(limit).all()

    def get_by_type_id_and_key(self, db: Session, type_id: int, key_value: str):
        """根据类型ID和键值获取字典枚举"""
        return db.query(self.model).filter(
            self.model.type_id == type_id,
            self.model.key_value == key_value,
            self.model.status == True
        ).first()

    def delete_by_type_id(self, db: Session, type_id: int):
        """根据类型ID删除所有字典枚举"""
        db.query(self.model).filter(self.model.type_id == type_id).delete()
        db.commit()


dictionary_type_crud = CRUDDictionaryType(DictionaryType)
dictionary_enum_crud = CRUDDictionaryEnum(DictionaryEnum)
