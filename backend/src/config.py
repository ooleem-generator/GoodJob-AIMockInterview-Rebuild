from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_API_KEY: str

    GOOGLE_APPLICATION_CREDENTIALS: str

    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    PORT: int = 8000
    RELOAD: bool = False

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
