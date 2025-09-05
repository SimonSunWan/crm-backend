from sqlalchemy import Column, String, Text, Date, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.base import TimestampMixin


class InternalOrder(Base, TimestampMixin):
    """保内工单模型"""
    
    __tablename__ = "internal_orders"
    
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
    under_warranty = Column(Boolean, default=True)
    fault_description = Column(Text)


class ExternalOrder(Base, TimestampMixin):
    """保外工单模型"""
    
    __tablename__ = "external_orders"
    
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
    under_warranty = Column(Boolean, default=False)
    fault_description = Column(Text)
