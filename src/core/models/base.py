from sqlalchemy.orm import DeclarativeBase

from core.models.audit_model import AuditModel
from core.utils.represent_instance import represent_instance


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        return represent_instance(self)


class BaseAuditModel(Base, AuditModel):
    __abstract__ = True
