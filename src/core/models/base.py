from sqlmodel import inspect

from core.models.audit import Audit


class BaseAudit(Audit):

    @classmethod
    def get_primary_key_name(cls) -> str | None:
        mapper = inspect(cls)
        pk_columns = [column.name for column in mapper.primary_key]
        return pk_columns[0] if pk_columns else None
