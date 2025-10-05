from typing import List, Optional

from app.schemas.base import ApiResponse, CamelCaseModel, Token


class UserBase(CamelCaseModel):

    email: Optional[str] = None
    phone: Optional[str] = None
    user_name: str
    nick_name: Optional[str] = None
    avatar: Optional[str] = None  # 头像URL
    status: bool
    roles: List[str]  # 角色编码数组


class UserCreate(UserBase):

    password: str


class UserUpdate(CamelCaseModel):

    email: Optional[str] = None
    phone: Optional[str] = None
    user_name: Optional[str] = None
    nick_name: Optional[str] = None
    avatar: Optional[str] = None  # 头像URL
    status: Optional[bool] = None
    roles: Optional[List[str]] = None  # 角色编码数组


class UserResponse(UserBase):

    id: int
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    role_names: Optional[List[str]] = None  # 角色名称数组
    departments: Optional[List[str]] = None  # 部门名称数组

    model_config = {"exclude": {"hashed_password"}}

    @classmethod
    def model_validate(cls, obj):
        """重写验证方法，处理角色数据转换"""
        # 创建数据字典，避免直接修改原对象
        data = {}

        # 复制基本字段
        for field in [
            "id",
            "email",
            "phone",
            "user_name",
            "nick_name",
            "avatar",
            "created_by",
            "updated_by",
        ]:
            if hasattr(obj, field):
                data[field] = getattr(obj, field)

        # 处理角色数据
        if hasattr(obj, "roles"):
            role_codes = [role.role_code for role in obj.roles] if obj.roles else []
            role_names = [role.role_name for role in obj.roles] if obj.roles else []
            data["roles"] = role_codes
            data["role_names"] = role_names
        else:
            data["roles"] = []
            data["role_names"] = []

        # 处理部门数据 - 包含部门成员和部门负责人
        department_names = []
        
        # 添加部门成员
        if hasattr(obj, "departments") and obj.departments:
            member_dept_names = [dept.dept_name for dept in obj.departments]
            department_names.extend(member_dept_names)
        
        # 添加部门负责人
        if hasattr(obj, "leading_departments") and obj.leading_departments:
            leader_dept_names = [dept.dept_name for dept in obj.leading_departments]
            department_names.extend(leader_dept_names)
        
        # 去重并保持顺序
        unique_departments = []
        for dept_name in department_names:
            if dept_name not in unique_departments:
                unique_departments.append(dept_name)
        
        data["departments"] = unique_departments

        # 处理status字段：已经是Boolean类型
        if hasattr(obj, "status"):
            data["status"] = obj.status
        else:
            data["status"] = True  # 默认值

        return super().model_validate(data)


class UserLogin(CamelCaseModel):
    user_name: str
    password: str


class UserRegister(CamelCaseModel):
    user_name: str
    nick_name: str
    phone: str
    email: Optional[str] = None
    password: str
    system_code: str


class UserForgetPassword(CamelCaseModel):
    username: str
    new_password: str
    system_code: str


class LoginResponse(ApiResponse):
    data: Token
