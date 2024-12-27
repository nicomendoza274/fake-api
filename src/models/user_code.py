from sqlmodel import Field

from core.models.base import BaseAudit


class UserCode(BaseAudit, table=True):
    __tablename__ = "user_codes"  # type: ignore
    user_code_id: int | None = Field(primary_key=True)
    code: int
    user_id: int | None = Field(foreign_key="users.user_id", nullable=True)
