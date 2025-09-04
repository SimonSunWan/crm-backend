from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime
from app.core.crud import CRUDBase
from app.models.order import InternalOrder, ExternalOrder


class InternalOrderCRUD(CRUDBase[InternalOrder]):
    """保内工单CRUD操作"""
    
    def generate_order_id(self, db: Session) -> str:
        """生成保内工单ID：BN + 年月日 + 4位自增"""
        today = datetime.now().strftime("%Y%m%d")
        prefix = f"BN{today}"
        
        latest_order = (
            db.query(self.model)
            .filter(self.model.id.like(f"{prefix}%"))
            .order_by(desc(self.model.id))
            .first()
        )
        
        if latest_order:
            latest_num = int(latest_order.id[-4:])
            new_num = latest_num + 1
        else:
            new_num = 1
            
        return f"{prefix}{new_num:04d}"
    
    def create(self, db: Session, obj_in: dict) -> InternalOrder:
        """创建保内工单"""
        order_id = self.generate_order_id(db)
        obj_in['id'] = order_id
        return super().create(db, obj_in)
    
    def get_by_id(self, db: Session, order_id: str) -> Optional[InternalOrder]:
        """根据工单ID获取保内工单"""
        return db.query(self.model).filter(self.model.id == order_id).first()


class ExternalOrderCRUD(CRUDBase[ExternalOrder]):
    """保外工单CRUD操作"""
    
    def generate_order_id(self, db: Session) -> str:
        """生成保外工单ID：BW + 年月日 + 4位自增"""
        today = datetime.now().strftime("%Y%m%d")
        prefix = f"BW{today}"
        
        latest_order = (
            db.query(self.model)
            .filter(self.model.id.like(f"{prefix}%"))
            .order_by(desc(self.model.id))
            .first()
        )
        
        if latest_order:
            latest_num = int(latest_order.id[-4:])
            new_num = latest_num + 1
        else:
            new_num = 1
            
        return f"{prefix}{new_num:04d}"
    
    def create(self, db: Session, obj_in: dict) -> ExternalOrder:
        """创建保外工单"""
        order_id = self.generate_order_id(db)
        obj_in['id'] = order_id
        return super().create(db, obj_in)
    
    def get_by_id(self, db: Session, order_id: str) -> Optional[ExternalOrder]:
        """根据工单ID获取保外工单"""
        return db.query(self.model).filter(self.model.id == order_id).first()


internal_order_crud = InternalOrderCRUD(InternalOrder)
external_order_crud = ExternalOrderCRUD(ExternalOrder)
