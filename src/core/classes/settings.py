import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Auth
    SECRET_KEY: str = str(os.getenv("SECRET_KEY"))
    TOKEN_EXPIRE_DAYS: int = 1
    TOKEN_ALGORITHM: str = "HS256"

    # Database
    DB_URI: str = str(os.getenv("DB_URI"))

    # Email
    DEFAULT_PORT: int = 587
    MAIL_USERNAME: str = str(os.getenv("MAIL_USERNAME"))
    MAIL_PASSWORD: str = str(os.getenv("MAIL_PASSWORD"))
    MAIL_FROM: str = str(os.getenv("MAIL_FROM"))
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", DEFAULT_PORT))
    MAIL_SERVER: str = str(os.getenv("MAIL_SERVER"))


settings = Settings()
