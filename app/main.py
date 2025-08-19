from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.api import api_router
from app.core.database import SessionLocal
from app.crud.user import user_crud
from app.schemas.base import ApiResponse
import traceback
import logging
from sqlalchemy import any_

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    db = SessionLocal()
    try:
        # 检查是否已存在超级管理员
        existing_admin = db.query(user_crud.model).filter(
            (user_crud.model.user_name == "Super") & ("SUPER" == any_(user_crud.model.roles))
        ).first()
        
        if not existing_admin:
            # 创建默认超级管理员
            admin_data = {
                "email": "super@example.com",
                "phone": "18888888888",
                "user_name": "Super",
                "nick_name": "超级管理员",
                "password": "Super@3000",
                "status": True,
                "roles": ["SUPER"]
            }
            user_crud.create(db, admin_data)
    finally:
        db.close()
    
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_PRE_STR}/openapi.json",
    lifespan=lifespan,
)

# 先注册中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 然后注册异常处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP异常处理器"""
    logger.error(f"HTTP异常: {exc.status_code} - {exc.detail}")
    error_response = ApiResponse(
        code=exc.status_code,
        message=exc.detail,
        data=None
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"全局异常: {exc}")
    logger.error(f"异常详情: {traceback.format_exc()}")
    error_response = ApiResponse(
        code=500,
        message=f"服务器内部错误: {str(exc)}",
        data=None
    )
    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )

# 最后注册路由
app.include_router(api_router, prefix=settings.API_PRE_STR)
