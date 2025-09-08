from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime
from app.core.crud import CRUDBase
from app.models.order import InternalOrder, ExternalOrder, InternalOrderDetail, ExternalOrderDetail


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
    
    def create_with_details(self, db: Session, order_data: dict, detail_data: dict = None) -> InternalOrder:
        """创建工单并关联详情记录"""
        # 创建主工单
        order = self.create(db, order_data)
        
        # 如果有详情数据，创建详情记录
        if detail_data:
            detail_data['order_id'] = order.id
            detail = InternalOrderDetail(**detail_data)
            db.add(detail)
            db.commit()
            db.refresh(detail)
        
        return order

    def update_with_details(self, db: Session, order_id: str, order_data: dict, detail_data: dict = None) -> Optional[InternalOrder]:
        """更新工单并关联详情记录"""
        # 更新主工单
        order = self.get_by_id(db, order_id)
        if not order:
            return None
            
        for field, value in order_data.items():
            setattr(order, field, value)
        
        # 更新或创建详情记录
        if detail_data:
            detail = db.query(InternalOrderDetail).filter(InternalOrderDetail.order_id == order_id).first()
            if detail:
                for field, value in detail_data.items():
                    setattr(detail, field, value)
            else:
                detail_data['order_id'] = order_id
                detail = InternalOrderDetail(**detail_data)
                db.add(detail)
        
        db.commit()
        db.refresh(order)
        return order

    def get_with_details(self, db: Session, order_id: str) -> Optional[InternalOrder]:
        """获取工单及其详情记录"""
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
    
    def create_with_details(self, db: Session, order_data: dict, detail_data: dict = None) -> ExternalOrder:
        """创建工单并关联详情记录"""
        # 创建主工单
        order = self.create(db, order_data)
        
        # 如果有详情数据，创建详情记录
        if detail_data:
            detail_data['order_id'] = order.id
            detail = ExternalOrderDetail(**detail_data)
            db.add(detail)
            db.commit()
            db.refresh(detail)
        
        return order

    def update_with_details(self, db: Session, order_id: str, order_data: dict, detail_data: dict = None) -> Optional[ExternalOrder]:
        """更新工单并关联详情记录"""
        # 更新主工单
        order = self.get_by_id(db, order_id)
        if not order:
            return None
            
        for field, value in order_data.items():
            setattr(order, field, value)
        
        # 更新或创建详情记录
        if detail_data:
            detail = db.query(ExternalOrderDetail).filter(ExternalOrderDetail.order_id == order_id).first()
            if detail:
                for field, value in detail_data.items():
                    setattr(detail, field, value)
            else:
                detail_data['order_id'] = order_id
                detail = ExternalOrderDetail(**detail_data)
                db.add(detail)
        
        db.commit()
        db.refresh(order)
        return order


internal_order_crud = InternalOrderCRUD(InternalOrder)
external_order_crud = ExternalOrderCRUD(ExternalOrder)
