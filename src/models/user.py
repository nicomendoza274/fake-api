from datetime import datetime

from pydantic import Field, model_validator
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import Field, Relationship, and_

from core.models.base import BaseAudit
from core.models.camel import Camel
from core.models.file import File, FileDTO
from core.models.user import UserBase, UserModel
from core.utils.encrypt import encrypt_string


class UserResponseDTO(UserBase):
    user_id: int
    role_id: int | None = None
    picture: FileDTO | None = None


class UserDTO(UserBase):
    user_id: SkipJsonSchema[int] | None = Field(default=None, exclude=True)
    role_id: int | None = None
    password: str
    hash: SkipJsonSchema[str] | None = Field(default=None, repr=True)

    @model_validator(mode="after")
    def compute_hash(cls, values):
        values.hash = encrypt_string(values.password)
        return values


class UserUpdateDTO(Camel):
    first_name: str
    last_name: str
    email: str
    picture_id: int | None = None


class UserChangePasswordDTO(Camel):
    new_password: str
    hash: SkipJsonSchema[str] | None = Field(default=None, exclude=True)

    @model_validator(mode="after")
    def compute_hash(cls, values):
        values.hash = encrypt_string(values.new_password)
        return values


class User(UserModel, BaseAudit, table=True):
    __tablename__ = "users"  # type: ignore

    # role_id: int | None = Field(default=None, exclude=True)
    picture: File | None = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": lambda: and_(
                File.file_id == User.picture_id,
                File.deleted_at == None,
            )
        }
    )


class UserJWT(Camel):
    user_id: int
    email: str
    role_id: int | None = None
    picture_id: int | None = None


class UserLoginDTO(Camel):
    email: str
    password: str
    hash: SkipJsonSchema[str] | None = Field(default=None, exclude=True)

    @model_validator(mode="after")
    def compute_hash(cls, values):
        values.hash = encrypt_string(values.password)
        return values


class UserLoggedDTO(Camel):
    user_id: int
    user_name: str | None = None
    email: str
    token: str | None = None
    expiration_date: datetime | None = None
    refresh_token: str = ""
    role_id: int | None = None
    picture_url: str | None = None
    id: str | None = None


class UserForgotPasswordDTO(Camel):
    email: str


class UserCheckCodeDTO(Camel):
    recovery_code: str
    email: str


class UserResetPasswordDTO(Camel):
    recovery_code: str
    email: str
    password: str
    hash: SkipJsonSchema[str] | None = Field(default=None, exclude=True)

    @model_validator(mode="after")
    def compute_hash(cls, values):
        values.hash = encrypt_string(values.password)
        return values
