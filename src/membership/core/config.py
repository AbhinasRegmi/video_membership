import os
from typing import List
from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings,  SettingsConfigDict


os.environ.setdefault("CQLENG_ALLOW_SCHEMA_MANAGEMENT", "1")

class _Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    #path variables
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent #root of proj
    TEMPLATE_DIR: str = os.path.join(BASE_DIR, 'templates')
    STATIC_DIR: str = os.path.join(BASE_DIR, 'static')

    #cors variables
    CORS_ALLOWED_ORIGINS: List[str] = [
        "https://abhinasregmi.com.np",
        "http://localhost:8000"
    ]

    # db variables
    CASSANDRA_DB_KEYSPACE: str
    CASSANDRA_DB_CLIENT_ID: str
    CASSANDRA_DB_CLIENT_SECRET: str
    CASSANDRA_DB_ENCRYPTED_BUNDLE: str = os.path.join('.', 'encrypted', 'astradb_connect.zip')

    #jwt variables
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXP: int = 1 # 30 minutes

    # .env
    MEMBERSHIP_SECRET_KEY: str
    
@lru_cache(maxsize=1)
def _settings() -> _Setting:
    return _Setting() #type:ignore

settings = _settings()