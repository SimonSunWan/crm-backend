from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import UserDisabledError
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """验证令牌"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None


def authenticate_user(db: Session, user_name: str, password: str) -> Optional[User]:
    """验证用户凭据"""
    user = db.query(User).filter(User.user_name == user_name).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None

    # 检查用户是否有启用的角色
    if user.roles:
        enabled_roles = [role for role in user.roles if role.status]
        if not enabled_roles:
            raise UserDisabledError("您的角色已被禁用")

    return user


def get_current_user(token: str, db: Session) -> Optional[User]:
    """根据token获取当前用户"""
    payload = verify_token(token)
    if payload is None:
        return None
    user_id = payload.get("sub")
    if user_id is None:
        return None
    user = db.query(User).filter(User.id == int(user_id)).first()
    return user


def check_user_permissions(user: User, required_role_codes: list) -> bool:
    """检查用户权限"""
    user_role_codes = [role.role_code for role in user.roles if role.status]
    return any(role_code in user_role_codes for role_code in required_role_codes)
