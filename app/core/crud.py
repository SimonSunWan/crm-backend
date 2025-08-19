from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    """通用 CRUD 操作基类"""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """根据 ID 获取单个记录"""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """获取多个记录"""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: dict) -> ModelType:
        """创建新记录"""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_or_404(self, db: Session, id: int, error_message: str = "记录未找到") -> ModelType:
        """获取记录，如果不存在则返回 404 错误"""
        obj = self.get(db, id)
        if obj is None:
            raise HTTPException(status_code=404, detail=error_message)
        return obj

    def update(self, db: Session, db_obj: ModelType, obj_in: dict) -> ModelType:
        """更新记录"""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: ModelType) -> None:
        """删除记录"""
        db.delete(db_obj)
        db.commit()
