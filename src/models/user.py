from datetime import datetime

from fastapi import Form, UploadFile
from pydantic import Field, model_validator
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import Field, Index, Relationship, and_

from src.core.models.base import BaseAudit
from src.core.models.camel import Camel
from src.core.models.file import File, FileDTO
from src.core.models.user import UserBase, UserModel
from src.core.utils.encrypt import encrypt_string
from src.models.role import Role, RoleResponseDTO
from src.models.user_role import UserRole


class UserResponseDTO(UserBase):
    roles: list[RoleResponseDTO] = []
    picture: FileDTO | None = None


class UserDTO(UserBase):
    user_id: SkipJsonSchema[int] | None = Field(default=None, exclude=True)
    password: str = Field(exclude=True)
    hash: SkipJsonSchema[str] | None = Field(default=None, repr=True)

    @model_validator(mode="after")
    def compute_hash(cls, values):
        values.hash = encrypt_string(values.password)
        return values


class CreateUserDTO(Camel):
    data: str = Form(...)
    picture: UploadFile | None = None


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
    __tablename__: str = "users"

    roles: list[Role] | None = Relationship(
        link_model=UserRole,
        sa_relationship_kwargs={
            "primaryjoin": lambda: and_(
                UserRole.user_id == User.user_id,
                UserRole.deleted_at == None,
            )
        },
    )
    picture: File | None = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": lambda: and_(
                File.file_id == User.picture_id,
                File.deleted_at == None,
            ),
        }
    )

    # Database indexes for better performance
    __table_args__ = (
        Index("idx_user_email", "email"),  # For login queries
        Index("idx_user_deleted_at", "deleted_at"),  # For soft delete queries
        Index("idx_user_created_at", "created_at"),  # For audit queries
        Index("idx_user_hash", "hash"),  # For authentication queries
    )


class UserJWT(Camel):
    user_id: int
    email: str
    roles: list[RoleResponseDTO] | None = None
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
    roles: list[RoleResponseDTO] | None = None
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
