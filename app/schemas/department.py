from typing import List, Optional

from app.schemas.base import CamelCaseModel


class DepartmentBase(CamelCaseModel):
    """部门基础模型"""

    dept_name: str
    parent_id: Optional[int] = None
    level: int = 1
    path: Optional[str] = None
    sort_order: int = 0
    leader_ids: Optional[List[int]] = None
    member_ids: Optional[List[int]] = None
    status: bool = True


class DepartmentCreate(CamelCaseModel):
    """创建部门模型"""

    dept_name: str
    parent_id: Optional[int] = None
    sort_order: int = 0
    leader_ids: Optional[List[int]] = None
    member_ids: Optional[List[int]] = None
    status: bool = True


class DepartmentUpdate(CamelCaseModel):
    """更新部门模型"""

    dept_name: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: Optional[int] = None
    leader_ids: Optional[List[int]] = None
    member_ids: Optional[List[int]] = None
    status: Optional[bool] = None


class DepartmentResponse(DepartmentBase):
    """部门响应模型"""

    id: int
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    children: Optional[List["DepartmentResponse"]] = None
    leader_names: Optional[List[str]] = None
    member_names: Optional[List[str]] = None
    user_count: int = 0

    @classmethod
    def model_validate(cls, obj, **kwargs):
        """重写验证方法，处理关联数据转换"""
        if isinstance(obj, dict):
            return super().model_validate(obj, **kwargs)
        
        data = cls._extract_basic_fields(obj)
        data.update(cls._extract_leader_info(obj))
        data.update(cls._extract_member_info(obj))
        data.update(cls._extract_children_info(obj, cls))

        return super().model_validate(data, **kwargs)

    @staticmethod
    def _extract_basic_fields(obj):
        """提取基本字段"""
        field_mapping = {
            "id": "id",
            "dept_name": "deptName",
            "parent_id": "parentId",
            "level": "level",
            "path": "path",
            "sort_order": "sortOrder",
            "status": "status",
            "created_by": "createdBy",
            "updated_by": "updatedBy",
        }
        
        return {
            model_field: getattr(obj, db_field)
            for db_field, model_field in field_mapping.items()
            if hasattr(obj, db_field)
        }

    @staticmethod
    def _extract_leader_info(obj):
        """提取负责人信息"""
        if hasattr(obj, "leaders") and obj.leaders:
            return {
                "leaderIds": [leader.id for leader in obj.leaders],
                "leaderNames": [leader.nick_name or leader.user_name for leader in obj.leaders]
            }
        return {"leaderIds": [], "leaderNames": []}

    @staticmethod
    def _extract_member_info(obj):
        """提取成员信息"""
        if hasattr(obj, "users") and obj.users:
            return {
                "memberIds": [user.id for user in obj.users],
                "memberNames": [user.nick_name or user.user_name for user in obj.users],
                "userCount": len(obj.users)
            }
        return {"memberIds": [], "memberNames": [], "userCount": 0}

    @staticmethod
    def _extract_children_info(obj, cls):
        """提取子部门信息"""
        if hasattr(obj, "children") and obj.children:
            return {"children": [cls.model_validate(child) for child in obj.children]}
        return {"children": []}


# 解决循环引用
DepartmentResponse.model_rebuild()
