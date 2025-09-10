from typing import Any, Dict, Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.crud import CRUDBase
from app.core.exceptions import UserAlreadyExistsError
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CRUDUser(CRUDBase[User]):
    """用户 CRUD 操作"""

    def create(self, db: Session, obj_in: Dict[str, Any]) -> User:
        """创建用户，自动处理密码加密"""
        user_data = obj_in.copy()

        # 检查用户名是否已存在
        if self.get_by_username(db, user_data.get("user_name")):
            raise UserAlreadyExistsError("用户名已存在")

        # 检查邮箱是否已存在
        if user_data.get("email") and self.get_by_email(db, user_data.get("email")):
            raise UserAlreadyExistsError("邮箱已存在")

        # 检查手机号是否已存在
        if user_data.get("phone") and self.get_by_phone(db, user_data.get("phone")):
            raise UserAlreadyExistsError("手机号已存在")

        # 处理密码加密
        if "password" in user_data:
            user_data["hashed_password"] = pwd_context.hash(user_data.pop("password"))

        return super().create(db, user_data)

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return db.query(User).filter(User.user_name == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()

    def get_by_phone(self, db: Session, phone: str) -> Optional[User]:
        """根据手机号获取用户"""
        return db.query(User).filter(User.phone == phone).first()

    def authenticate(self, db: Session, username: str, password: str) -> Optional[User]:
        """验证用户凭据"""
        user = self.get_by_username(db, username)
        if not user:
            return None
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return user

    def update_password(self, db: Session, user: User, new_password: str) -> User:
        """更新用户密码"""
        user.hashed_password = pwd_context.hash(new_password)
        db.commit()
        db.refresh(user)
        return user


user_crud = CRUDUser(User)
