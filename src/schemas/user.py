from datetime import datetime

from core.schemas.camel import CamelModel


class UserBaseSchema(CamelModel):
    user_id: int | None
    first_name: str
    last_name: str
    email: str
    role_id: int | None = None

    class Config:
        from_attributes = True


class UserResponseDTO(UserBaseSchema):
    user_id: int


class UserDTO(UserBaseSchema):
    password: str
    user_id: int | None = None


class UserJWT(CamelModel):
    user_id: int
    email: str
    role_id: int | None = None

    class Config:
        from_attributes = True


class UserLoginDTO(CamelModel):
    email: str
    password: str


class UserLoggedDTO(CamelModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    token: str | None = None
    expiration_date: datetime | None = None
    role_id: int | None = None

    class Config:
        from_attributes = True


class UserSendCodeDTO(CamelModel):
    email: str


class UserValidateCodeDTO(CamelModel):
    code: str
    email: str


class UserForgotChangePasswordDTO(CamelModel):
    code: str
    email: str
    newPassword: str
