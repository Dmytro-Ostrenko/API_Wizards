import os
from typing import Any

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_DB: str = os.getenv('POSTGRES_DB')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_PORT: str = os.getenv('POSTGRES_PORT')
    POSTGRES_DOMAIN: str = os.getenv('POSTGRES_DOMAIN')
    DB_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_DOMAIN}:{POSTGRES_PORT}/{POSTGRES_DB}"       
    SECRET_KEY_JWT: str = os.getenv('SECRET_KEY_JWT')
    ALGORITHM: str = os.getenv('ALGORITHM')
    MAIL_USERNAME: EmailStr = "postgres@meail.com"
    MAIL_PASSWORD: str = os.getenv('MAIL_PASSWORD')
    MAIL_FROM: str = os.getenv('MAIL_FROM')
    MAIL_PORT: int = os.getenv('MAIL_PORT')
    MAIL_SERVER: str = os.getenv('MAIL_SERVER')
    REDIS_DOMAIN: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    cloud_name: str = os.getenv('cloud_name')
    api_key: str = os.getenv('api_key')
    api_secret: str = os.getenv('api_secret')
    



    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v: Any):
        if v not in ["HS256", "HS512"]:
            raise ValueError("algorithm must be HS256 or HS512")
        return v
    
    model_config = ConfigDict(extra='ignore', env_file=".env", env_file_encoding="utf-8")  # noqa
    

config = Settings()