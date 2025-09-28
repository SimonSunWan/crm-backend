from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class InternalOrder(Base, TimestampMixin):
    """保内工单模型"""

    __tablename__ = "internal_order"

    id = Column(String, primary_key=True, index=True)
    customer = Column(String, nullable=False)
    vehicle_model = Column(String, nullable=False)
    repair_shop = Column(String, nullable=False)
    reporter_name = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    report_date = Column(Date, nullable=False)
    project_type = Column(String, nullable=False)
    project_stage = Column(String, nullable=False)
    license_plate = Column(String)
    vin_number = Column(String, nullable=False)
    mileage = Column(Float, default=0.0)
    vehicle_location = Column(Text)
    vehicle_date = Column(Date)
    pack_code = Column(String)
    pack_date = Column(Date)
    seal_code = Column(String)
    under_warranty = Column(Boolean, default=True)
    fault_description = Column(Text)
    order_progress = Column(Text)  # 工单进度
    is_end = Column(Boolean, default=False)  # 是否完成所有步骤
    created_by = Column(Integer, ForeignKey("user.id"), nullable=True)

    details = relationship(
        "InternalOrderDetail", back_populates="order", cascade="all, delete-orphan"
    )


class InternalOrderDetail(Base, TimestampMixin):
    """保内工单详情记录模型"""

    __tablename__ = "internal_order_detail"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(
        String, ForeignKey("internal_order.id"), nullable=False, index=True
    )

    # 维修记录字段
    repair_person = Column(String)
    repair_date = Column(Date)
    avic_responsibility = Column(Boolean, default=True)
    fault_classification = Column(String)
    fault_location = Column(String)
    part_category = Column(String)
    part_location = Column(String)
    repair_description = Column(Text)

    # 详情记录字段
    spare_part_location = Column(String)
    spare_parts = Column(JSON)  # 备件使用详情
    costs = Column(JSON)  # 费用使用详情
    labors = Column(JSON)  # 工时详情
    cost_remarks = Column(JSON)  # 费用使用备注

    # 关联主工单
    order = relationship("InternalOrder", back_populates="details")


class ExternalOrder(Base, TimestampMixin):
    """保外工单模型"""

    __tablename__ = "external_order"

    id = Column(String, primary_key=True, index=True)
    customer = Column(String, nullable=False)
    vehicle_model = Column(String, nullable=False)
    repair_shop = Column(String, nullable=False)
    reporter_name = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    report_date = Column(Date, nullable=False)
    insurer = Column(String, nullable=False)
    assessor = Column(String, nullable=False)
    license_plate = Column(String)
    vin_number = Column(String, nullable=False)
    mileage = Column(Float, default=0.0)
    vehicle_location = Column(Text)
    vehicle_date = Column(Date)
    pack_code = Column(String)
    pack_date = Column(Date)
    seal_code = Column(String)
    under_warranty = Column(Boolean, default=False)
    fault_description = Column(Text)
    order_progress = Column(Text)  # 工单进度
    is_end = Column(Boolean, default=False)  # 是否完成所有步骤
    created_by = Column(Integer, ForeignKey("user.id"), nullable=True)

    # 关联详情记录
    details = relationship(
        "ExternalOrderDetail", back_populates="order", cascade="all, delete-orphan"
    )


class ExternalOrderDetail(Base, TimestampMixin):
    """保外工单详情记录模型"""

    __tablename__ = "external_order_detail"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(
        String, ForeignKey("external_order.id"), nullable=False, index=True
    )

    # 维修记录字段
    repair_person = Column(String)
    repair_date = Column(Date)
    avic_responsibility = Column(Boolean, default=True)
    repair_description = Column(Text)
    fault_location = Column(String)

    # 详情记录字段
    spare_part_location = Column(String)
    spare_parts = Column(JSON)  # 备件使用详情
    costs = Column(JSON)  # 费用使用详情
    labors = Column(JSON)  # 工时详情
    repair_progress = Column(String)  # 维修进度（从工时详情中移出）
    cost_remarks = Column(JSON)  # 费用使用备注

    # 关联主工单
    order = relationship("ExternalOrder", back_populates="details")
