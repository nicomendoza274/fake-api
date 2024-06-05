from datetime import datetime

from pydantic import BaseModel


class AuditSchema(BaseModel):
    created_at: datetime | None = None
    created_by: int | None = None
    updated_at: datetime | None = None
    updated_by: int | None = None
    deleted_at: datetime | None = None
    deleted_by: int | None = None
