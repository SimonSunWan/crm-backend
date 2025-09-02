from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = "crm-backend"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "CRM后端系统"
    API_PRE_STR: str = "/api"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:

        if isinstance(v, str) and not v.startswith("["):

            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):

            return v
        raise ValueError(v)

    DATABASE_URL: str

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    model_config = {"case_sensitive": True, "env_file": ".env"}


settings = Settings()
