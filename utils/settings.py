import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DEFAULT_PORT: int = 5432
    # Enviroment
    ENVIROMENT: str = str(os.getenv("ENVIROMENT"))

    # Auth
    MY_SECRET_KEY: str = str(os.getenv("MY_SECRET_KEY"))
    # TOKEN_EXPIRE_MINUTES: int = os.getenv("TOKEN_EXPIRE_MINUTES")

    # Database
    DB_NAME: str = str(os.getenv("DB_NAME"))
    DB_USER: str = str(os.getenv("DB_USER"))
    DB_PASS: str = str(os.getenv("DB_PASS"))
    DB_HOST: str = str(os.getenv("DB_HOST"))
    DB_PORT: int = int(os.getenv("DB_PORT", DEFAULT_PORT))
