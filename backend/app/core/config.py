import os
from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "TraceBit"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    BACKEND_CORS_ORIGINS: List[str] = [os.environ.get("CORS_ORIGINS")]

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
