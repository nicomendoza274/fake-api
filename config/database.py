from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

from config.config import DevelopmentConfig, ProductionConfig
from utils.settings import Settings

settings = Settings()

if settings.ENVIROMENT == "production":
    conf = ProductionConfig
    database_url = conf.DATABASE_URI

else:
    conf = DevelopmentConfig
    database_url = conf.DATABASE_URI

engine = create_engine(database_url)

Session = sessionmaker(bind=engine)
Base = declarative_base()


# Dependency
def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()
