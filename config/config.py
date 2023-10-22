import os

from utils.settings import Settings

settings = Settings()


class ProductionConfig:
    DATABASE_URI = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.DB_NAME}"
    DEBUG = False


class DevelopmentConfig:
    sqlite_file_name = "../database.sqlite"
    base_dir = os.path.dirname(os.path.realpath(__file__))
    DATABASE_URI = f"sqlite:///{os.path.join(base_dir,sqlite_file_name)}"
    DEBUG = True
