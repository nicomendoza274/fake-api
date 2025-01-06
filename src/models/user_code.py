from sqlmodel import BigInteger, Field

from core.models.base import BaseAudit


class UserCode(BaseAudit, table=True):
    __tablename__: str = "user_codes"
    user_code_id: int | None = Field(sa_type=BigInteger, default=None, primary_key=True)
    code: int
    user_id: int | None = Field(foreign_key="users.user_id", nullable=True)
