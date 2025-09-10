from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import field_serializer, field_validator

from app.schemas.base import CamelCaseModel


class OrderBase(CamelCaseModel):
    """工单基础模型"""

    customer: str
    vehicle_model: str
    repair_shop: str
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

    @field_validator("vehicle_date", "pack_date", mode="before")
    @classmethod
    def validate_date_fields(cls, v):
        """处理空字符串日期字段"""
        if v == "" or v is None:
            return None
        return v


class OrderDetailBase(CamelCaseModel):
    """工单详情基础模型"""

    repair_person: Optional[str] = None
    repair_date: Optional[date] = None
    avic_responsibility: Optional[bool] = True
    fault_classification: Optional[str] = None
    fault_location: Optional[str] = None
    part_category: Optional[str] = None
    part_location: Optional[str] = None
    repair_description: Optional[str] = None
    spare_part_location: Optional[str] = None
    spare_parts: Optional[List[Dict[str, Any]]] = None
    costs: Optional[List[Dict[str, Any]]] = None
    labors: Optional[List[Dict[str, Any]]] = None

    @field_validator("repair_date", mode="before")
    @classmethod
    def validate_repair_date(cls, v):
        """处理空字符串日期字段"""
        if v == "" or v is None:
            return None
        return v


class InternalOrderCreate(OrderBase):
    """保内工单创建模型"""

    under_warranty: bool = True
    # 详情记录字段
    repair_person: Optional[str] = None
    repair_date: Optional[date] = None
    avic_responsibility: Optional[bool] = True
    fault_classification: Optional[str] = None
    fault_location: Optional[str] = None
    part_category: Optional[str] = None
    part_location: Optional[str] = None
    repair_description: Optional[str] = None
    spare_part_location: Optional[str] = None
    spare_parts: Optional[List[Dict[str, Any]]] = None
    costs: Optional[List[Dict[str, Any]]] = None
    labors: Optional[List[Dict[str, Any]]] = None


class ExternalOrderCreate(OrderBase):
    """保外工单创建模型"""

    under_warranty: bool = False
    # 详情记录字段
    repair_person: Optional[str] = None
    repair_date: Optional[date] = None
    avic_responsibility: Optional[bool] = True
    fault_classification: Optional[str] = None
    fault_location: Optional[str] = None
    part_category: Optional[str] = None
    part_location: Optional[str] = None
    repair_description: Optional[str] = None
    spare_part_location: Optional[str] = None
    spare_parts: Optional[List[Dict[str, Any]]] = None
    costs: Optional[List[Dict[str, Any]]] = None
    labors: Optional[List[Dict[str, Any]]] = None


class InternalOrderUpdate(CamelCaseModel):
    """保内工单更新模型"""

    customer: Optional[str] = None
    vehicle_model: Optional[str] = None
    repair_shop: Optional[str] = None
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
    # 详情记录字段
    repair_person: Optional[str] = None
    repair_date: Optional[date] = None
    avic_responsibility: Optional[bool] = None
    fault_classification: Optional[str] = None
    fault_location: Optional[str] = None
    part_category: Optional[str] = None
    part_location: Optional[str] = None
    repair_description: Optional[str] = None
    spare_part_location: Optional[str] = None
    spare_parts: Optional[List[Dict[str, Any]]] = None
    costs: Optional[List[Dict[str, Any]]] = None
    labors: Optional[List[Dict[str, Any]]] = None

    @field_validator("vehicle_date", "pack_date", "repair_date", mode="before")
    @classmethod
    def validate_date_fields(cls, v):
        """处理空字符串日期字段"""
        if v == "" or v is None:
            return None
        return v


class ExternalOrderUpdate(CamelCaseModel):
    """保外工单更新模型"""

    customer: Optional[str] = None
    vehicle_model: Optional[str] = None
    repair_shop: Optional[str] = None
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
    # 详情记录字段
    repair_person: Optional[str] = None
    repair_date: Optional[date] = None
    avic_responsibility: Optional[bool] = None
    fault_classification: Optional[str] = None
    fault_location: Optional[str] = None
    part_category: Optional[str] = None
    part_location: Optional[str] = None
    repair_description: Optional[str] = None
    spare_part_location: Optional[str] = None
    spare_parts: Optional[List[Dict[str, Any]]] = None
    costs: Optional[List[Dict[str, Any]]] = None
    labors: Optional[List[Dict[str, Any]]] = None

    @field_validator("vehicle_date", "pack_date", "repair_date", mode="before")
    @classmethod
    def validate_date_fields(cls, v):
        """处理空字符串日期字段"""
        if v == "" or v is None:
            return None
        return v


class InternalOrderDetailResponse(CamelCaseModel):
    """保内工单详情响应模型"""

    id: int
    order_id: str
    repair_person: Optional[str] = None
    repair_date: Optional[date] = None
    avic_responsibility: Optional[bool] = True
    fault_classification: Optional[str] = None
    fault_location: Optional[str] = None
    part_category: Optional[str] = None
    part_location: Optional[str] = None
    repair_description: Optional[str] = None
    spare_part_location: Optional[str] = None
    spare_parts: Optional[List[Dict[str, Any]]] = None
    costs: Optional[List[Dict[str, Any]]] = None
    labors: Optional[List[Dict[str, Any]]] = None
    create_time: datetime
    update_time: Optional[datetime] = None

    @field_serializer("create_time", "update_time")
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """序列化datetime为yyyy-MM-dd HH:mm:ss格式"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")

    @field_serializer("repair_date")
    def serialize_date(self, value: Optional[date]) -> Optional[str]:
        """序列化date为yyyy-MM-dd格式"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d")


class InternalOrderResponse(CamelCaseModel):
    """保内工单响应模型"""

    id: str
    customer: str
    vehicle_model: str
    repair_shop: str
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
    # 详情记录
    details: Optional[List[InternalOrderDetailResponse]] = None

    @field_serializer("create_time", "update_time")
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """序列化datetime为yyyy-MM-dd HH:mm:ss格式"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")

    @field_serializer("report_date", "vehicle_date", "pack_date")
    def serialize_date(self, value: Optional[date]) -> Optional[str]:
        """序列化date为yyyy-MM-dd格式"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d")


class ExternalOrderDetailResponse(CamelCaseModel):
    """保外工单详情响应模型"""

    id: int
    order_id: str
    repair_person: Optional[str] = None
    repair_date: Optional[date] = None
    avic_responsibility: Optional[bool] = True
    fault_classification: Optional[str] = None
    fault_location: Optional[str] = None
    part_category: Optional[str] = None
    part_location: Optional[str] = None
    repair_description: Optional[str] = None
    spare_part_location: Optional[str] = None
    spare_parts: Optional[List[Dict[str, Any]]] = None
    costs: Optional[List[Dict[str, Any]]] = None
    labors: Optional[List[Dict[str, Any]]] = None
    create_time: datetime
    update_time: Optional[datetime] = None

    @field_serializer("create_time", "update_time")
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """序列化datetime为yyyy-MM-dd HH:mm:ss格式"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")

    @field_serializer("repair_date")
    def serialize_date(self, value: Optional[date]) -> Optional[str]:
        """序列化date为yyyy-MM-dd格式"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d")


class ExternalOrderResponse(CamelCaseModel):
    """保外工单响应模型"""

    id: str
    customer: str
    vehicle_model: str
    repair_shop: str
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
    # 详情记录
    details: Optional[List[ExternalOrderDetailResponse]] = None

    @field_serializer("create_time", "update_time")
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """序列化datetime为yyyy-MM-dd HH:mm:ss格式"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")

    @field_serializer("report_date", "vehicle_date", "pack_date")
    def serialize_date(self, value: Optional[date]) -> Optional[str]:
        """序列化date为yyyy-MM-dd格式"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d")
