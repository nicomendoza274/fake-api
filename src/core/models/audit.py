from datetime import datetime
from typing import Optional

from sqlalchemy import TIMESTAMP, BigInteger
from sqlmodel import Field, SQLModel


class Audit(SQLModel):
    created_at: Optional[datetime] = Field(
        default=None,
        nullable=True,
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
    )
    created_by: Optional[int] = Field(
        default=None,
        foreign_key="users.user_id",
        sa_type=BigInteger,
        nullable=True,
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        nullable=True,
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
    )
    updated_by: Optional[int] = Field(
        default=None,
        foreign_key="users.user_id",
        sa_type=BigInteger,
        nullable=True,
    )
    deleted_at: Optional[datetime] = Field(
        default=None, nullable=True, sa_type=TIMESTAMP(timezone=True)  # type: ignore
    )
    deleted_by: Optional[int] = Field(
        default=None,
        foreign_key="users.user_id",
        sa_type=BigInteger,
        nullable=True,
    )
