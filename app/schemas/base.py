from datetime import date, datetime
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, field_serializer

T = TypeVar("T")


def to_camel_case(snake_str: str) -> str:
    """将下划线命名转换为驼峰命名"""
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class CamelCaseModel(BaseModel):
    """支持驼峰命名的基础模型"""

    model_config = ConfigDict(
        alias_generator=to_camel_case, populate_by_name=True, from_attributes=True
    )
    
    def model_dump(self, **kwargs):
        """默认使用by_alias=True"""
        if 'by_alias' not in kwargs:
            kwargs['by_alias'] = True
        return super().model_dump(**kwargs)


class TimestampMixin(BaseModel):
    """时间戳混入类，提供时间字段的序列化"""

    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    @field_serializer("create_time", "update_time")
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """序列化datetime为yyyy-MM-dd HH:mm:ss格式"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")


class DateMixin(BaseModel):
    """日期混入类，提供日期字段的序列化"""

    report_date: Optional[date] = None
    vehicle_date: Optional[date] = None
    pack_date: Optional[date] = None

    @field_serializer("report_date", "vehicle_date", "pack_date")
    def serialize_date(self, value: Optional[date]) -> Optional[str]:
        """序列化date为yyyy-MM-dd格式"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d")


class BaseResponse(BaseModel):
    """基础响应模型"""

    id: int
    create_time: datetime
    update_time: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ApiResponse(CamelCaseModel, Generic[T]):
    """统一API响应格式"""

    code: int = 200
    message: str = "操作成功"
    data: Optional[T] = None


class PaginatedResponse(CamelCaseModel, Generic[T]):
    """分页响应模型"""

    records: list[T]
    total: int
    current: int
    size: int


class Token(CamelCaseModel):
    """令牌模型"""

    access_token: str
    token_type: str = "Bearer"


class ErrorResponse(CamelCaseModel):
    """错误响应模型"""

    code: int
    message: str
    detail: Optional[str] = None
