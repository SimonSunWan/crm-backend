import random
import time
from datetime import datetime
from typing import Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

from app.core.crud import CRUDBase
from app.core.exceptions import CRMException
from app.core.id_generator import order_id_generator
from app.models.order import (
    ExternalOrder,
    ExternalOrderDetail,
    InternalOrder,
    InternalOrderDetail,
)


class InternalOrderCRUD(CRUDBase[InternalOrder]):
    """保内工单CRUD操作"""

    def generate_order_id_safe(self, db: Session, max_retries: int = 5) -> str:
        """并发安全的保内工单ID生成：BN + 年月日 + 4位自增"""
        today = datetime.now().strftime("%Y%m%d")
        prefix = f"BN{today}"

        for attempt in range(max_retries):
            try:
                # 使用数据库锁确保并发安全
                with db.begin_nested():  # 使用嵌套事务
                    # 查询并锁定相关记录
                    latest_order = (
                        db.query(self.model)
                        .filter(self.model.id.like(f"{prefix}%"))
                        .with_for_update()  # 添加行级锁
                        .order_by(desc(self.model.id))
                        .first()
                    )

                    if latest_order:
                        latest_num = int(latest_order.id[-4:])
                        new_num = latest_num + 1
                    else:
                        new_num = 1

                    order_id = f"{prefix}{new_num:04d}"

                    # 验证ID唯一性（双重检查）
                    existing_order = (
                        db.query(self.model).filter(self.model.id == order_id).first()
                    )
                    if not existing_order:
                        return order_id
                    else:
                        # ID已存在，等待一小段时间后重试
                        time.sleep(random.uniform(0.01, 0.05))
                        continue

            except Exception as e:
                if attempt == max_retries - 1:
                    raise CRMException(
                        status_code=500, detail=f"生成工单ID失败: {str(e)}"
                    )
                # 等待后重试
                time.sleep(random.uniform(0.01, 0.1))
                continue

        # 如果所有重试都失败，抛出异常
        raise CRMException(status_code=500, detail="生成工单ID失败，请稍后重试")

    def create(self, db: Session, obj_in: dict) -> InternalOrder:
        """创建保内工单（使用并发安全的ID生成）"""
        try:
            order_id = order_id_generator.generate_internal_order_id(db)
            obj_in["id"] = order_id
            return super().create(db, obj_in)
        except Exception as e:
            db.rollback()
            if (
                "unique constraint" in str(e).lower()
                or "duplicate key" in str(e).lower()
            ):
                # ID冲突，使用备用策略重试
                order_id = order_id_generator.generate_with_timestamp("BN")
                obj_in["id"] = order_id
                return super().create(db, obj_in)
            else:
                raise CRMException(
                    status_code=500, detail=f"创建保内工单失败: {str(e)}"
                )

    def get_by_id(self, db: Session, order_id: str) -> Optional[InternalOrder]:
        """根据工单ID获取保内工单"""
        return db.query(self.model).filter(self.model.id == order_id).first()

    def create_with_details(
        self, db: Session, order_data: dict, detail_data: dict = None
    ) -> InternalOrder:
        """创建工单并关联详情记录"""
        # 创建主工单
        order = self.create(db, order_data)

        # 如果有详情数据，创建详情记录
        if detail_data:
            detail_data["order_id"] = order.id
            detail = InternalOrderDetail(**detail_data)
            db.add(detail)
            db.commit()
            db.refresh(detail)

        return order

    def update_with_details(
        self, db: Session, order_id: str, order_data: dict, detail_data: dict = None
    ) -> Optional[InternalOrder]:
        """更新工单并关联详情记录"""
        # 更新主工单
        order = self.get_by_id(db, order_id)
        if not order:
            return None

        for field, value in order_data.items():
            setattr(order, field, value)

        # 更新或创建详情记录
        if detail_data:
            detail = (
                db.query(InternalOrderDetail)
                .filter(InternalOrderDetail.order_id == order_id)
                .first()
            )
            if detail:
                for field, value in detail_data.items():
                    setattr(detail, field, value)
            else:
                detail_data["order_id"] = order_id
                detail = InternalOrderDetail(**detail_data)
                db.add(detail)

        db.commit()
        db.refresh(order)
        return order

    def get_with_details(self, db: Session, order_id: str) -> Optional[InternalOrder]:
        """获取工单及其详情记录"""
        return (
            db.query(self.model)
            .options(joinedload(self.model.details))
            .filter(self.model.id == order_id)
            .first()
        )


class ExternalOrderCRUD(CRUDBase[ExternalOrder]):
    """保外工单CRUD操作"""

    def generate_order_id_safe(self, db: Session, max_retries: int = 5) -> str:
        """并发安全的保外工单ID生成：BW + 年月日 + 4位自增"""
        today = datetime.now().strftime("%Y%m%d")
        prefix = f"BW{today}"

        for attempt in range(max_retries):
            try:
                # 使用数据库锁确保并发安全
                with db.begin_nested():  # 使用嵌套事务
                    # 查询并锁定相关记录
                    latest_order = (
                        db.query(self.model)
                        .filter(self.model.id.like(f"{prefix}%"))
                        .with_for_update()  # 添加行级锁
                        .order_by(desc(self.model.id))
                        .first()
                    )

                    if latest_order:
                        latest_num = int(latest_order.id[-4:])
                        new_num = latest_num + 1
                    else:
                        new_num = 1

                    order_id = f"{prefix}{new_num:04d}"

                    # 验证ID唯一性（双重检查）
                    existing_order = (
                        db.query(self.model).filter(self.model.id == order_id).first()
                    )
                    if not existing_order:
                        return order_id
                    else:
                        # ID已存在，等待一小段时间后重试
                        time.sleep(random.uniform(0.01, 0.05))
                        continue

            except Exception as e:
                if attempt == max_retries - 1:
                    raise CRMException(
                        status_code=500, detail=f"生成工单ID失败: {str(e)}"
                    )
                # 等待后重试
                time.sleep(random.uniform(0.01, 0.1))
                continue

        # 如果所有重试都失败，抛出异常
        raise CRMException(status_code=500, detail="生成工单ID失败，请稍后重试")

    def create(self, db: Session, obj_in: dict) -> ExternalOrder:
        """创建保外工单（使用并发安全的ID生成）"""
        try:
            order_id = order_id_generator.generate_external_order_id(db)
            obj_in["id"] = order_id
            return super().create(db, obj_in)
        except Exception as e:
            db.rollback()
            if (
                "unique constraint" in str(e).lower()
                or "duplicate key" in str(e).lower()
            ):
                # ID冲突，使用备用策略重试
                order_id = order_id_generator.generate_with_timestamp("BW")
                obj_in["id"] = order_id
                return super().create(db, obj_in)
            else:
                raise CRMException(
                    status_code=500, detail=f"创建保外工单失败: {str(e)}"
                )

    def get_by_id(self, db: Session, order_id: str) -> Optional[ExternalOrder]:
        """根据工单ID获取保外工单"""
        return db.query(self.model).filter(self.model.id == order_id).first()

    def create_with_details(
        self, db: Session, order_data: dict, detail_data: dict = None
    ) -> ExternalOrder:
        """创建工单并关联详情记录"""
        # 创建主工单
        order = self.create(db, order_data)

        # 如果有详情数据，创建详情记录
        if detail_data:
            detail_data["order_id"] = order.id
            detail = ExternalOrderDetail(**detail_data)
            db.add(detail)
            db.commit()
            db.refresh(detail)

        return order

    def update_with_details(
        self, db: Session, order_id: str, order_data: dict, detail_data: dict = None
    ) -> Optional[ExternalOrder]:
        """更新工单并关联详情记录"""
        # 更新主工单
        order = self.get_by_id(db, order_id)
        if not order:
            return None

        for field, value in order_data.items():
            setattr(order, field, value)

        # 更新或创建详情记录
        if detail_data:
            detail = (
                db.query(ExternalOrderDetail)
                .filter(ExternalOrderDetail.order_id == order_id)
                .first()
            )
            if detail:
                for field, value in detail_data.items():
                    setattr(detail, field, value)
            else:
                detail_data["order_id"] = order_id
                detail = ExternalOrderDetail(**detail_data)
                db.add(detail)

        db.commit()
        db.refresh(order)
        return order

    def get_with_details(self, db: Session, order_id: str) -> Optional[ExternalOrder]:
        """获取工单及其详情记录"""
        return (
            db.query(self.model)
            .options(joinedload(self.model.details))
            .filter(self.model.id == order_id)
            .first()
        )


internal_order_crud = InternalOrderCRUD(InternalOrder)
external_order_crud = ExternalOrderCRUD(ExternalOrder)
