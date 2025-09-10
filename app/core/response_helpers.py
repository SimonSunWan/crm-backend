"""
公共响应处理函数
提供统一的API响应处理
"""
from typing import Any, List, Dict
from fastapi import HTTPException
from app.schemas.base import ApiResponse
from app.models.user import User


def success_response(message: str = "操作成功", data: Any = None, code: int = 200) -> ApiResponse:
    """
    创建成功响应
    
    Args:
        message: 响应消息
        data: 响应数据
        code: 响应代码
        
    Returns:
        ApiResponse: 成功响应对象
    """
    return ApiResponse(code=code, message=message, data=data)


def error_response(message: str = "操作失败", code: int = 500, data: Any = None) -> ApiResponse:
    """
    创建错误响应
    
    Args:
        message: 错误消息
        code: 错误代码
        data: 错误数据
        
    Returns:
        ApiResponse: 错误响应对象
    """
    return ApiResponse(code=code, message=message, data=data)


def handle_api_exception(func):
    """
    API异常处理装饰器
    
    Args:
        func: 被装饰的函数
        
    Returns:
        装饰后的函数
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{func.__name__}失败: {str(e)}")
    return wrapper


def set_audit_fields(data: Dict[str, Any], current_user: User, operation: str = "create") -> Dict[str, Any]:
    """
    设置审计字段（创建者/更新者）
    
    Args:
        data: 数据字典
        current_user: 当前用户
        operation: 操作类型（create/update）
        
    Returns:
        Dict[str, Any]: 包含审计字段的数据字典
    """
    if operation == "create":
        data["created_by"] = current_user.user_name
    elif operation == "update":
        data["updated_by"] = current_user.user_name
    return data


def normalize_empty_strings(data: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
    """
    将空字符串转换为None，避免唯一约束冲突
    
    Args:
        data: 数据字典
        fields: 需要处理的字段列表
        
    Returns:
        Dict[str, Any]: 处理后的数据字典
    """
    for field in fields:
        if field in data and data[field] == '':
            data[field] = None
    return data


def build_pagination_response(records: List[Any], total: int, current: int, size: int) -> Dict[str, Any]:
    """
    构建分页响应数据
    
    Args:
        records: 记录列表
        total: 总记录数
        current: 当前页码
        size: 每页大小
        
    Returns:
        Dict[str, Any]: 分页响应数据
    """
    return {
        "records": records,
        "total": total,
        "current": current,
        "size": size
    }


def apply_pagination_filter(query, current: int, size: int):
    """
    应用分页过滤
    
    Args:
        query: SQLAlchemy查询对象
        current: 当前页码
        size: 每页大小
        
    Returns:
        tuple: (分页后的查询, 总记录数)
    """
    skip = (current - 1) * size
    total = query.count()
    paginated_query = query.offset(skip).limit(size)
    return paginated_query, total
