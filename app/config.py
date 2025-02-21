import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    UPLOAD_DIR: str
    UPLOAD_DIR_ANIMAL_TYPE: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env.local" if os.getenv("ENV") != "docker" else ".env.docker"  # Selecciona el archivo según el entorno

settings = Settings()