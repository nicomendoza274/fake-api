from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.session import sessionmaker

from core.classes.settings import settings

DATABASE_URI = settings.DB_URI

engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)


def represent_instance(instance):
    attributes = ", ".join(
        f"{attribute}={getattr(instance, attribute)}"
        for attribute in inspect(instance).attrs.keys()
    )
    class_name = instance.__class__.__name__
    return f"<{class_name}({attributes})>"


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        return represent_instance(self)


# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
