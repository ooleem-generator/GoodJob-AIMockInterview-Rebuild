from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_API_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str | None = None  # Optional, for admin operations

    # Google Cloud (optional)
    GOOGLE_APPLICATION_CREDENTIALS: str | None = None

    # LangSmith
    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_TRACING: str | None = None

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Server
    PORT: int = 8000
    RELOAD: bool = False

    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DATABASE_URL: str

    # Clerk Authentication
    CLERK_FRONTEND_URL: str
    CLERK_WEBHOOK_SECRET: str | None = None  # Required for webhook verification

    # Environment
    ENV: str = "local"  # local, production

    class Config:
        # Load .env.local for local development, .env.production for production
        # Default to .env.local if ENV is not set
        env_file = os.getenv("ENV_FILE", ".env.local")
        env_file_encoding = "utf-8"


settings = Settings()
