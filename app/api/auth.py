from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import authenticate_user, create_access_token
from app.core.database import get_db
from app.core.exceptions import InvalidCredentialsError, UserDisabledError
from app.schemas.base import Token
from app.schemas.user import LoginResponse, UserLogin

router = APIRouter()


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    user = authenticate_user(db, user_credentials.user_name, user_credentials.password)
    if not user:
        raise InvalidCredentialsError("用户名或密码错误")

    if not user.status:
        raise UserDisabledError("用户未启用")

    access_token = create_access_token(data={"sub": str(user.id)})
    return LoginResponse(message="登录成功", data=Token(access_token=access_token))
