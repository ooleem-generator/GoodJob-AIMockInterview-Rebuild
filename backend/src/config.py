from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str

    GOOGLE_APPLICATION_CREDENTIALS: str

    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    PORT: int = 8000
    RELOAD: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
