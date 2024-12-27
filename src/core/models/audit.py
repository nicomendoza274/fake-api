from datetime import datetime

from sqlmodel import Field, SQLModel, func


class AuditModel(SQLModel):
    created_at: datetime | None = Field(default_factory=func.now, nullable=True)
    created_by: int | None = Field(
        default=None, foreign_key="users.user_id", nullable=True
    )
    updated_at: datetime | None = Field(default=None, nullable=True)
    updated_by: int | None = Field(
        default=None, foreign_key="users.user_id", nullable=True
    )
    deleted_at: datetime | None = Field(default=None, nullable=True)
    deleted_by: int | None = Field(default=None, nullable=True)
