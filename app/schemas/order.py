from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from app.schemas.base import CamelCaseModel


class OrderBase(CamelCaseModel):
    """工单基础模型"""
    customer: str
    reporter_name: str
    contact_info: str
    report_date: date
    project_type: str
    project_stage: str
    license_plate: Optional[str] = None
    vin_number: str
    mileage: Optional[float] = 0.0
    vehicle_location: Optional[str] = None
    vehicle_date: Optional[date] = None
    pack_code: Optional[str] = None
    pack_date: Optional[date] = None
    fault_description: Optional[str] = None


class InternalOrderCreate(OrderBase):
    """保内工单创建模型"""
    under_warranty: bool = True


class ExternalOrderCreate(OrderBase):
    """保外工单创建模型"""
    under_warranty: bool = False


class InternalOrderUpdate(CamelCaseModel):
    """保内工单更新模型"""
    customer: Optional[str] = None
    reporter_name: Optional[str] = None
    contact_info: Optional[str] = None
    report_date: Optional[date] = None
    project_type: Optional[str] = None
    project_stage: Optional[str] = None
    license_plate: Optional[str] = None
    vin_number: Optional[str] = None
    mileage: Optional[float] = None
    vehicle_location: Optional[str] = None
    vehicle_date: Optional[date] = None
    pack_code: Optional[str] = None
    pack_date: Optional[date] = None
    under_warranty: Optional[bool] = None
    fault_description: Optional[str] = None


class ExternalOrderUpdate(CamelCaseModel):
    """保外工单更新模型"""
    customer: Optional[str] = None
    reporter_name: Optional[str] = None
    contact_info: Optional[str] = None
    report_date: Optional[date] = None
    project_type: Optional[str] = None
    project_stage: Optional[str] = None
    license_plate: Optional[str] = None
    vin_number: Optional[str] = None
    mileage: Optional[float] = None
    vehicle_location: Optional[str] = None
    vehicle_date: Optional[date] = None
    pack_code: Optional[str] = None
    pack_date: Optional[date] = None
    under_warranty: Optional[bool] = None
    fault_description: Optional[str] = None


class InternalOrderResponse(CamelCaseModel):
    """保内工单响应模型"""
    id: str
    customer: str
    reporter_name: str
    contact_info: str
    report_date: date
    project_type: str
    project_stage: str
    license_plate: Optional[str] = None
    vin_number: str
    mileage: Optional[float] = 0.0
    vehicle_location: Optional[str] = None
    vehicle_date: Optional[date] = None
    pack_code: Optional[str] = None
    pack_date: Optional[date] = None
    under_warranty: bool = True
    fault_description: Optional[str] = None
    create_time: datetime
    update_time: Optional[datetime] = None


class ExternalOrderResponse(CamelCaseModel):
    """保外工单响应模型"""
    id: str
    customer: str
    reporter_name: str
    contact_info: str
    report_date: date
    project_type: str
    project_stage: str
    license_plate: Optional[str] = None
    vin_number: str
    mileage: Optional[float] = 0.0
    vehicle_location: Optional[str] = None
    vehicle_date: Optional[date] = None
    pack_code: Optional[str] = None
    pack_date: Optional[date] = None
    under_warranty: bool = False
    fault_description: Optional[str] = None
    create_time: datetime
    update_time: Optional[datetime] = None
