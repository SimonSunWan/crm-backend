from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime
import re


def to_camel_case(snake_str: str) -> str:
    """将下划线命名转换为驼峰命名"""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class CamelCaseModel(BaseModel):
    """支持驼峰命名的基础模型"""
    model_config = ConfigDict(
        alias_generator=to_camel_case,
        populate_by_name=True,
        from_attributes=True
    )


class BaseResponse(BaseModel):
    """基础响应模型"""
    id: int
    create_time: datetime
    update_time: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ApiResponse(CamelCaseModel):
    """统一API响应格式"""
    code: int = 200
    message: str = "操作成功"
    data: Optional[Any] = None


class Token(CamelCaseModel):
    """令牌模型"""
    access_token: str
    token_type: str = "Bearer"
