from app.core.crud import CRUDBase
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CRUDUser(CRUDBase[User]):
    """用户 CRUD 操作"""

    def create(self, db, obj_in: dict):
        """创建用户，自动处理密码加密"""
        user_data = obj_in.copy()
        user_data["hashed_password"] = pwd_context.hash(user_data.pop("password"))
        return super().create(db, user_data)


user_crud = CRUDUser(User)
