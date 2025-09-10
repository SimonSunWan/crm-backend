import logging
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.api import api_router
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.exceptions import CRMException
from app.core.middleware import LoggingMiddleware, SecurityHeadersMiddleware
from app.schemas.base import ApiResponse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""

    db = SessionLocal()
    try:
        import asyncio

        from scripts.init_system import system_code_scheduler

        asyncio.create_task(system_code_scheduler())
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)


@app.exception_handler(CRMException)
async def crm_exception_handler(request: Request, exc: CRMException):
    """CRM自定义异常处理器"""
    logger.error(f"CRM异常: {exc.status_code} - {exc.detail}")
    error_response = ApiResponse(code=exc.status_code, message=exc.detail, data=None)
    return JSONResponse(
        status_code=exc.status_code, content=error_response.model_dump()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP异常处理器"""
    logger.error(f"HTTP异常: {exc.status_code} - {exc.detail}")
    error_response = ApiResponse(code=exc.status_code, message=exc.detail, data=None)
    return JSONResponse(
        status_code=exc.status_code, content=error_response.model_dump()
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"全局异常: {exc}")
    logger.error(f"异常详情: {traceback.format_exc()}")
    error_response = ApiResponse(
        code=500, message=f"服务器内部错误: {str(exc)}", data=None
    )
    return JSONResponse(status_code=500, content=error_response.model_dump())


app.include_router(api_router, prefix=settings.API_PRE_STR)
