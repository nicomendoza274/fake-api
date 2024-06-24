from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from core.classes.settings import settings

DATABASE_URI = settings.DB_URI

engine = create_engine(DATABASE_URI)

session = sessionmaker(bind=engine)


# Dependency
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
