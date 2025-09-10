from typing import Optional

from app.schemas.base import CamelCaseModel


class RoleBase(CamelCaseModel):
    """角色基础模型"""

    role_name: str
    role_code: str
    description: Optional[str] = None
    status: bool = True


class RoleCreate(RoleBase):
    """创建角色模型"""

    pass


class RoleUpdate(CamelCaseModel):
    """更新角色模型"""

    role_name: Optional[str] = None
    role_code: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None


class RoleResponse(RoleBase):
    """角色响应模型"""

    id: int
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
