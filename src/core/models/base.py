from sqlalchemy.orm import DeclarativeBase

from core.utils.represent_instance import represent_instance


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        return represent_instance(self)
