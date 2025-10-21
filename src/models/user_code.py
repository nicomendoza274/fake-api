from sqlmodel import BigInteger, Field

from core.models.base import BaseAudit


class UserCode(BaseAudit, table=True):
    __tablename__: str = "user_codes"

    user_code_id: int | None = Field(
        default=None,
        primary_key=True,
        sa_type=BigInteger,
    )
    code: int
    user_id: int | None = Field(
        foreign_key="users.user_id",
        nullable=True,
        sa_type=BigInteger,
    )
