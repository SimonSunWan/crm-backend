"""公共响应处理函数"""

from typing import Any, Dict, List

from fastapi import HTTPException

from app.models.user import User


def handle_api_exception(func):
    """API异常处理装饰器"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"操作失败: {str(e)}")

    return wrapper


def set_audit_fields(
    data: Dict[str, Any], current_user: User, operation: str = "create"
) -> Dict[str, Any]:
    """设置审计字段（创建者/更新者）"""
    field_map = {"create": "created_by", "update": "updated_by"}
    if operation in field_map:
        data[field_map[operation]] = current_user.user_name
    return data


def normalize_empty_strings(data: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
    """将空字符串转换为None，避免唯一约束冲突"""
    for field in fields:
        if field in data and data[field] == "":
            data[field] = None
    return data


def build_pagination_response(
    records: List[Any], total: int, current: int, size: int
) -> Dict[str, Any]:
    """构建分页响应数据"""
    return {"records": records, "total": total, "current": current, "size": size}


def apply_pagination_filter(query, current: int, size: int):
    """应用分页过滤"""
    skip = (current - 1) * size
    total = query.count()
    return query.offset(skip).limit(size), total
