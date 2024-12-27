from sqlmodel import BigInteger, Field

from core.models.camel import Camel


class UserBase(Camel):
    first_name: str = Field()
    last_name: str = Field()
    email: str = Field(unique=True)
    picture_id: int | None = Field(
        default=None, foreign_key="files.file_id", nullable=True
    )


class UserModel(UserBase):
    user_id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    hash: str = Field()
