import os
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Auth
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "your-secret-key-here-must-be-very-long-and-secure"
    )
    TOKEN_EXPIRE_DAYS: int = int(os.getenv("TOKEN_EXPIRE_DAYS", "1"))
    TOKEN_ALGORITHM: str = os.getenv("TOKEN_ALGORITHM", "HS256")

    # Database
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "fake_api_db")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")

    # Email
    DEFAULT_PORT: int = 587
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", str(DEFAULT_PORT)))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "")

    # Security
    ALLOWED_ORIGINS: str = os.getenv(
        "ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080"
    )
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    ALLOWED_FILE_TYPES: str = os.getenv(
        "ALLOWED_FILE_TYPES", "image/jpeg,image/png,image/gif,application/pdf"
    )

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
