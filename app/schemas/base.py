from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class BaseResponse(BaseModel):
    """基础响应模型"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ApiResponse(BaseModel):
    """统一API响应格式"""
    code: int = 200
    message: str = "操作成功"
    data: Optional[Any] = None


class Token(BaseModel):
    """令牌模型"""
    access_token: str
    token_type: str = "bearer"
