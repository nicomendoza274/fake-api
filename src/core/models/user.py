import sqlalchemy as sa
from sqlmodel import BigInteger, Field

from src.core.models.camel import Camel


class UserBase(Camel):
    user_id: int | None = Field(sa_type=BigInteger, default=None, primary_key=True)
    first_name: str = Field(sa_column=sa.Column(sa.String, nullable=False))
    last_name: str = Field(sa_column=sa.Column(sa.String, nullable=False))
    email: str = Field(sa_column=sa.Column(sa.String, unique=True, nullable=False))
    picture_id: int | None = Field(
        default=None,
        sa_column=sa.Column(
            sa.BigInteger,
            sa.ForeignKey("files.file_id", use_alter=True, deferrable=True),
            nullable=True,
        ),
    )


class UserModel(UserBase):
    hash: str = Field(sa_column=sa.Column(sa.String, nullable=False))
