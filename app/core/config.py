from typing import List, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类"""

    PROJECT_NAME: str = "crm-backend"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "CRM后端系统"
    API_PRE_STR: str = "/api"
    DEBUG: bool = False

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """组装CORS源列表"""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v

    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 12

    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0
    REDIS_MAX_CONNECTIONS: int = 20
    REDIS_SOCKET_TIMEOUT: int = 5
    REDIS_SOCKET_CONNECT_TIMEOUT: int = 5

    # 缓存配置
    CACHE_DEFAULT_TTL: int = 3600  # 默认缓存1小时
    CACHE_USER_TTL: int = 1800  # 用户信息缓存30分钟
    CACHE_MENU_TTL: int = 7200  # 菜单缓存2小时
    CACHE_DICTIONARY_TTL: int = 3600  # 字典缓存1小时

    model_config = {"case_sensitive": True, "env_file": ".env"}


settings = Settings()
