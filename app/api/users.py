from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.core.auth import get_current_user, get_password_hash, verify_password
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserRegister, UserForgetPassword
from app.schemas.base import ApiResponse, CamelCaseModel
from app.crud.user import user_crud
from app.models.user import User

router = APIRouter()


class ChangePasswordRequest(CamelCaseModel):
    currentPassword: str
    newPassword: str


def get_current_user_dependency(authorization: str = Header(...), db: Session = Depends(get_db)) -> User:
    """获取当前登录用户的依赖函数"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="无效的认证头")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="无效的token或用户不存在")
    # 检查用户状态：'1'表示启用，'2'表示禁用
    if user.status != '1':
        raise HTTPException(status_code=400, detail="用户未启用")
    return user


@router.get("/me", response_model=ApiResponse)
def get_current_user_info(current_user: User = Depends(get_current_user_dependency)):
    """获取当前登录用户的个人信息"""
    try:
        return ApiResponse(data=UserResponse.model_validate(current_user))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户信息失败: {str(e)}")


@router.put("/me", response_model=ApiResponse)
def update_current_user_info(
    user_update: UserUpdate, 
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """更新当前登录用户的个人信息"""
    try:
        # 处理角色数据
        update_data = user_update.model_dump(exclude_unset=True)
        role_codes = update_data.pop('roles', None)
        
        # 将空字符串转换为None，避免唯一约束冲突
        if 'email' in update_data and update_data['email'] == '':
            update_data['email'] = None
        
        # 不允许通过此接口修改角色
        if role_codes is not None:
            raise HTTPException(status_code=400, detail="不允许通过此接口修改角色")
        
        # 检查邮箱唯一性（排除当前用户）
        if 'email' in update_data and update_data['email']:
            existing_user = db.query(User).filter(
                User.email == update_data['email'],
                User.id != current_user.id
            ).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="邮箱已存在")
        
        # 检查用户名唯一性（排除当前用户）
        if 'user_name' in update_data:
            existing_username = db.query(User).filter(
                User.user_name == update_data['user_name'],
                User.id != current_user.id
            ).first()
            if existing_username:
                raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 处理status字段：将布尔值转换为字符串
        if 'status' in update_data:
            update_data['status'] = '1' if update_data['status'] else '2'
        
        # 更新用户基本信息
        updated_user = user_crud.update(db, current_user, update_data)
        
        return ApiResponse(message="用户信息更新成功", data=UserResponse.model_validate(updated_user))
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新用户信息失败: {str(e)}")


@router.put("/me/change-password", response_model=ApiResponse)
def change_current_user_password(
    password_request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """修改当前登录用户的密码"""
    try:
        # 验证当前密码
        if not verify_password(password_request.currentPassword, current_user.hashed_password):
            raise HTTPException(status_code=400, detail="当前密码错误")
        
        # 更新密码
        current_user.hashed_password = get_password_hash(password_request.newPassword)
        db.add(current_user)
        db.commit()
        
        return ApiResponse(message="密码修改成功")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"修改密码失败: {str(e)}")


@router.get("/", response_model=ApiResponse)
def get_users(
    current: int = 1, 
    size: int = 100, 
    userName: str = None,
    nickName: str = None,
    phone: str = None,
    email: str = None,
    roleCode: str = None,
    status: bool = None,
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    try:
        skip = (current - 1) * size
        
        # 构建基础查询
        query = db.query(User)
        
        # 过滤掉超级管理员用户（通过角色关联）
        from app.models.role import Role
        super_admin_role = db.query(Role).filter(Role.role_code == "SUPER").first()
        
        if super_admin_role:
            query = query.filter(~User.roles.any(Role.id == super_admin_role.id))
        
        # 添加筛选条件
        if userName:
            query = query.filter(User.user_name == userName)
        
        if nickName:
            query = query.filter(User.nick_name.ilike(f'%{nickName}%'))
        
        if phone:
            query = query.filter(User.phone.contains(phone))
        
        if email:
            query = query.filter(User.email.contains(email))
        
        if roleCode:
            # 通过角色关联筛选用户
            from app.models.role import Role
            role = db.query(Role).filter(Role.role_code == roleCode).first()
            if role:
                query = query.filter(User.roles.any(Role.id == role.id))
        
        if status is not None:
            # 将布尔值转换为字符串进行筛选
            status_str = '1' if status else '2'
            query = query.filter(User.status == status_str)
        
        # 预加载角色信息
        query = query.options(joinedload(User.roles))
        
        # 获取总数
        total = query.count()
        
        # 获取分页数据
        users = query.offset(skip).limit(size).all()
        
        # 将SQLAlchemy模型转换为Pydantic模型
        user_responses = [UserResponse.model_validate(user) for user in users]
        
        # 返回包含分页信息的响应
        response_data = {
            "records": user_responses,
            "total": total,
            "current": current,
            "size": size
        }
        
        return ApiResponse(data=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户列表失败: {str(e)}")


@router.post("/register", response_model=ApiResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    """用户注册"""
    try:
        # 校验系统码
        from app.crud.system_setting import system_setting_crud
        system_code_setting = system_setting_crud.get_by_key(db, setting_key="REGISTER_SYSTEM_CODE")
        if not system_code_setting or system_code_setting.setting_value != user.system_code:
            raise HTTPException(status_code=400, detail="系统码错误")
        
        # 检查用户名是否已存在
        existing_username = db.query(User).filter(User.user_name == user.user_name).first()
        if existing_username:
            raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 检查手机号是否已存在
        if user.phone:
            existing_phone = db.query(User).filter(User.phone == user.phone).first()
            if existing_phone:
                raise HTTPException(status_code=400, detail="手机号已存在")
        
        # 检查邮箱是否已存在（如果提供了邮箱）
        if user.email:
            existing_email = db.query(User).filter(User.email == user.email).first()
            if existing_email:
                raise HTTPException(status_code=400, detail="邮箱已存在")
        
        # 准备用户数据
        user_data = {
            'user_name': user.user_name,
            'nick_name': user.nick_name,
            'phone': user.phone,
            'email': user.email,
            'password': user.password,
            'status': '2',  # 默认未开启状态
            'roles': []  # 角色为空
        }
        
        # 创建用户
        created_user = user_crud.create(db, user_data)
        
        return ApiResponse(message="注册成功，请等待管理员审核", data=UserResponse.model_validate(created_user))
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"注册失败: {str(e)}")


@router.post("/", response_model=ApiResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """创建用户"""
    try:
        # 检查邮箱是否已存在（如果提供了邮箱）
        if user.email:
            existing_user = db.query(User).filter(User.email == user.email).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="邮箱已存在")
        
        # 检查用户名是否已存在
        existing_username = db.query(User).filter(User.user_name == user.user_name).first()
        if existing_username:
            raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 处理角色数据
        user_data = user.model_dump()
        role_codes = user_data.pop('roles', []) if isinstance(user_data.get('roles'), list) else []
        
        # 将空字符串转换为None，避免唯一约束冲突
        if 'email' in user_data and user_data['email'] == '':
            user_data['email'] = None
        
        # 检查是否尝试创建超级管理员用户
        if 'SUPER' in role_codes:
            raise HTTPException(status_code=400, detail="不允许创建超级管理员用户")
        
        # 处理status字段：将布尔值转换为字符串
        if 'status' in user_data:
            user_data['status'] = '1' if user_data['status'] else '2'
        
        # 创建用户
        created_user = user_crud.create(db, user_data)
        
        # 如果提供了角色编码，建立用户角色关联
        if role_codes:
            from app.models.role import Role
            roles = db.query(Role).filter(Role.role_code.in_(role_codes)).all()
            if roles:
                # 重新获取用户对象以确保它是有效的SQLAlchemy实例
                user_instance = db.query(User).filter(User.id == created_user.id).first()
                if user_instance:
                    user_instance.roles.extend(roles)
                    db.commit()
        
        return ApiResponse(message="用户创建成功", data=UserResponse.model_validate(created_user))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建用户失败: {str(e)}")


@router.get("/{user_id}", response_model=ApiResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """获取单个用户"""
    try:
        user = user_crud.get_or_404(db, user_id, "用户未找到")
        return ApiResponse(data=UserResponse.model_validate(user))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户失败: {str(e)}")


@router.put("/{user_id}", response_model=ApiResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """更新用户"""
    try:
        user = user_crud.get_or_404(db, user_id, "用户未找到")
        
        # 处理角色数据
        update_data = user_update.model_dump(exclude_unset=True)
        role_codes = update_data.pop('roles', None)
        
        # 将空字符串转换为None，避免唯一约束冲突
        if 'email' in update_data and update_data['email'] == '':
            update_data['email'] = None
        
        # 检查是否尝试将用户升级为超级管理员
        if role_codes and 'SUPER' in role_codes:
            raise HTTPException(status_code=400, detail="不允许将用户升级为超级管理员")
        
        # 检查邮箱唯一性（排除当前用户）
        if 'email' in update_data and update_data['email']:
            existing_user = db.query(User).filter(
                User.email == update_data['email'],
                User.id != user_id
            ).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="邮箱已存在")
        
        # 检查用户名唯一性（排除当前用户）
        if 'user_name' in update_data:
            existing_username = db.query(User).filter(
                User.user_name == update_data['user_name'],
                User.id != user_id
            ).first()
            if existing_username:
                raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 处理status字段：将布尔值转换为字符串
        if 'status' in update_data:
            update_data['status'] = '1' if update_data['status'] else '2'
        
        # 更新用户基本信息
        updated_user = user_crud.update(db, user, update_data)
        
        # 如果提供了角色编码，更新用户角色关联
        if role_codes is not None:
            from app.models.role import Role
            # 清空当前角色
            user.roles.clear()
            # 添加新角色
            if role_codes:
                roles = db.query(Role).filter(Role.role_code.in_(role_codes)).all()
                if roles:
                    user.roles.extend(roles)
            db.commit()
        
        return ApiResponse(message="用户更新成功", data=UserResponse.model_validate(updated_user))
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新用户失败: {str(e)}")


@router.delete("/{user_id}", response_model=ApiResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """删除用户"""
    try:
        user = user_crud.get_or_404(db, user_id, "用户未找到")
        user_crud.delete(db, user)
        return ApiResponse(message="用户删除成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除用户失败: {str(e)}")


@router.post("/forget-password", response_model=ApiResponse)
def forget_password(data: UserForgetPassword, db: Session = Depends(get_db)):
    """忘记密码重置"""
    try:
        # 校验系统码
        from app.crud.system_setting import system_setting_crud
        system_code_setting = system_setting_crud.get_by_key(db, setting_key="REGISTER_SYSTEM_CODE")
        if not system_code_setting or system_code_setting.setting_value != data.system_code:
            raise HTTPException(status_code=400, detail="系统码错误")
        
        # 查找用户
        user = db.query(User).filter(User.user_name == data.username).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 更新密码
        user.hashed_password = get_password_hash(data.new_password)
        db.commit()
        db.refresh(user)
        
        return ApiResponse(message="密码重置成功")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"密码重置失败: {str(e)}")
