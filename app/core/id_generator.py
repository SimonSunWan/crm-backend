# 并发安全的ID生成服务，提供多种ID生成策略，确保在高并发环境下的安全性

import random
import time
import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.exceptions import CRMException
from app.models.order import ExternalOrder, InternalOrder


class IDGenerationStrategy(Enum):
    """ID生成策略枚举"""

    DATABASE_LOCK = "database_lock"  # 数据库锁策略
    SEQUENCE = "sequence"  # 数据库序列策略
    UUID = "uuid"  # UUID策略
    REDIS_COUNTER = "redis_counter"  # Redis计数器策略


class OrderIDGenerator:
    """工单ID生成器"""

    def __init__(
        self, strategy: IDGenerationStrategy = IDGenerationStrategy.DATABASE_LOCK
    ):
        self.strategy = strategy

    def generate_internal_order_id(self, db: Session, max_retries: int = 5) -> str:
        """生成保内工单ID"""
        return self._generate_order_id(db, "BN", max_retries)

    def generate_external_order_id(self, db: Session, max_retries: int = 5) -> str:
        """生成保外工单ID"""
        return self._generate_order_id(db, "BW", max_retries)

    def _generate_order_id(self, db: Session, prefix: str, max_retries: int) -> str:
        """根据策略生成工单ID"""
        if self.strategy == IDGenerationStrategy.DATABASE_LOCK:
            return self._generate_with_database_lock(db, prefix, max_retries)
        elif self.strategy == IDGenerationStrategy.SEQUENCE:
            return self._generate_with_sequence(db, prefix)
        elif self.strategy == IDGenerationStrategy.UUID:
            return self._generate_with_uuid(prefix)
        else:
            raise ValueError(f"不支持的ID生成策略: {self.strategy}")

    def _generate_with_database_lock(
        self, db: Session, prefix: str, max_retries: int
    ) -> str:
        """使用数据库锁策略生成ID"""
        today = datetime.now().strftime("%Y%m%d")
        full_prefix = f"{prefix}{today}"

        for attempt in range(max_retries):
            try:
                # 使用数据库锁确保并发安全
                with db.begin_nested():
                    # 查询并锁定相关记录
                    latest_order = db.execute(
                        text(
                            f"""
                                SELECT id FROM {prefix.lower()}_orders
                                WHERE id LIKE :prefix
                                ORDER BY id DESC
                                LIMIT 1
                                FOR UPDATE
                            """
                        ),
                        {"prefix": f"{full_prefix}%"},
                    ).fetchone()

                    if latest_order:
                        latest_num = int(latest_order[0][-4:])
                        new_num = latest_num + 1
                    else:
                        new_num = 1

                    order_id = f"{full_prefix}{new_num:04d}"

                    # 验证ID唯一性
                    existing_order = db.execute(
                        text(
                            f"SELECT id FROM {prefix.lower()}_orders "
                            f"WHERE id = :order_id"
                        ),
                        {"order_id": order_id},
                    ).fetchone()

                    if not existing_order:
                        return order_id
                    else:
                        # ID已存在，等待后重试
                        time.sleep(random.uniform(0.01, 0.05))
                        continue

            except Exception as e:
                if attempt == max_retries - 1:
                    raise CRMException(
                        status_code=500, detail=f"生成工单ID失败: {str(e)}"
                    )
                time.sleep(random.uniform(0.01, 0.1))
                continue

        raise CRMException(status_code=500, detail="生成工单ID失败，请稍后重试")

    def _generate_with_sequence(self, db: Session, prefix: str) -> str:
        """使用数据库序列策略生成ID"""
        today = datetime.now().strftime("%Y%m%d")
        full_prefix = f"{prefix}{today}"

        # 创建序列（如果不存在）
        sequence_name = f"{prefix.lower()}_order_seq_{today}"

        try:
            # 尝试创建序列
            db.execute(text(f"CREATE SEQUENCE IF NOT EXISTS {sequence_name} START 1"))
            db.commit()

            # 获取下一个序列值
            result = db.execute(text(f"SELECT nextval('{sequence_name}')")).fetchone()
            sequence_value = result[0]

            return f"{full_prefix}{sequence_value:04d}"

        except Exception as e:
            raise CRMException(status_code=500, detail=f"使用序列生成ID失败: {str(e)}")

    def _generate_with_uuid(self, prefix: str) -> str:
        """使用UUID策略生成ID"""
        today = datetime.now().strftime("%Y%m%d")
        uuid_part = str(uuid.uuid4()).replace("-", "")[:8]  # 取UUID前8位
        return f"{prefix}{today}{uuid_part}"

    def generate_with_timestamp(self, prefix: str) -> str:
        """使用时间戳生成ID（适用于高频场景）"""
        timestamp = int(time.time() * 1000)  # 毫秒时间戳
        random_suffix = random.randint(1000, 9999)  # 4位随机数
        return f"{prefix}{timestamp}{random_suffix}"


# 全局ID生成器实例
order_id_generator = OrderIDGenerator(IDGenerationStrategy.DATABASE_LOCK)


class ConcurrentSafeOrderCRUD:
    """并发安全的工单CRUD操作基类"""

    def __init__(self, model_class, order_type: str):
        self.model_class = model_class
        self.order_type = order_type  # "internal" 或 "external"
        self.prefix = "BN" if order_type == "internal" else "BW"

    def generate_order_id(self, db: Session) -> str:
        """生成工单ID"""
        if self.order_type == "internal":
            return order_id_generator.generate_internal_order_id(db)
        else:
            return order_id_generator.generate_external_order_id(db)

    def create_order_safe(self, db: Session, obj_in: dict) -> any:
        """并发安全的创建工单"""
        try:
            # 生成ID
            order_id = self.generate_order_id(db)
            obj_in["id"] = order_id

            # 创建工单
            db_obj = self.model_class(**obj_in)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

            return db_obj

        except Exception as e:
            db.rollback()
            if (
                "unique constraint" in str(e).lower()
                or "duplicate key" in str(e).lower()
            ):
                # ID冲突，重试一次
                return self.create_order_safe(db, obj_in)
            else:
                raise CRMException(status_code=500, detail=f"创建工单失败: {str(e)}")


# 使用示例
def create_internal_order_safe(db: Session, order_data: dict):
    """并发安全的创建保内工单"""
    crud = ConcurrentSafeOrderCRUD(InternalOrder, "internal")
    return crud.create_order_safe(db, order_data)


def create_external_order_safe(db: Session, order_data: dict):
    """并发安全的创建保外工单"""
    crud = ConcurrentSafeOrderCRUD(ExternalOrder, "external")
    return crud.create_order_safe(db, order_data)
