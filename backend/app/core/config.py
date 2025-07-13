from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "TraceBit"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    BACKEND_CORS_ORIGINS: List[str] = ["https://tracebug.onrender.com"]

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
