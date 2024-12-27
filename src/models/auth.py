from datetime import datetime

from pydantic import Field, model_validator
from pydantic.json_schema import SkipJsonSchema

from core.models.camel import CamelModel
from core.utils.encrypt import encrypt_string


class UserJWT(CamelModel):
    user_id: int
    email: str
    role_id: int | None = None
    picture_id: int | None = None

    class Config:
        from_attributes = True


class UserLoginDTO(CamelModel):
    email: str
    password: str
    hash: SkipJsonSchema[str] | None = Field(default=None, exclude=True)

    @model_validator(mode="after")
    def compute_hash(cls, values):
        values.hash = encrypt_string(values.password)
        return values


class UserLoggedDTO(CamelModel):
    user_id: int
    user_name: str | None = None
    email: str
    token: str | None = None
    expiration_date: datetime | None = None
    refresh_token: str = ""
    role_id: int | None = None
    picture_url: str | None = None
    id: str | None = None
    display: None = None  # TODO: change this field
    id_valid: bool = True  # TODO: changes this field

    class Config:
        from_attributes = True


class UserForgotPasswordDTO(CamelModel):
    email: str


class UserCheckCodeDTO(CamelModel):
    recovery_code: str
    email: str


class UserResetPasswordDTO(CamelModel):
    recovery_code: str
    email: str
    password: str
    hash: SkipJsonSchema[str] | None = Field(default=None, exclude=True)

    @model_validator(mode="after")
    def compute_hash(cls, values):
        values.hash = encrypt_string(values.password)
        return values
