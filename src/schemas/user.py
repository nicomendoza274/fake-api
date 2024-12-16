from pydantic import Field, model_validator
from pydantic.json_schema import SkipJsonSchema

from core.schemas.camel import CamelModel
from core.schemas.file import FileDTO
from core.utils.encrypt import encrypt_string


class UserBase(CamelModel):
    first_name: str
    last_name: str
    email: str
    role_id: int | None = None
    picture_id: int | None = None

    class Config:
        from_attributes = True


class UserResponseDTO(UserBase):
    user_id: int
    picture: FileDTO | None = None


class UserDTO(UserBase):
    user_id: SkipJsonSchema[int] | None = Field(default=None, exclude=True)
    password: str
    hash: SkipJsonSchema[str] | None = Field(default=None, exclude=True)

    @model_validator(mode="after")
    def compute_hash(cls, values):
        values.hash = encrypt_string(values.password)
        return values


class UserUpdateDTO(CamelModel):
    first_name: str
    last_name: str
    email: str
    picture_id: int | None = None


class UserChangePasswordDTO(CamelModel):
    new_password: str
    hash: SkipJsonSchema[str] | None = Field(default=None, exclude=True)

    # model_config = {"json_schema_extra": {"examples": [{"newPassword": "string"}]}}

    @model_validator(mode="after")
    def compute_hash(cls, values):
        values.hash = encrypt_string(values.new_password)
        return values
