from typing import Optional

from sqlalchemy import Column

from schemas.camel import CamelModel


class User(CamelModel):
    email: str


class UserLogin(User):
    password: str


class UserLoged(User):
    user_id: int
    first_name: str
    last_name: str
    token: str
    role_id: int | None = None


class UserCreate(User):
    user_id: Optional[int] = None
    password: str
    first_name: str
    last_name: str
    role_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "test@gmail.com",
                "password": "b2xhIHF1ZSB0YWw=",
                "first_name": "Benjamin",
                "last_name": "Perez",
                "role_id": 1,
            }
        }


class UserCreated(User):
    user_id: int
    first_name: str
    last_name: str
    role_id: int | None = None


class UserList(User):
    user_id: int
    first_name: str
    last_name: str
    role_id: Optional[int] = None


class UserSendCode(User):
    class Config:
        json_schema_extra = {
            "example": {
                "email": "test@gmail.com",
            }
        }


class UserValidateCode(User):
    code: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "test@gmail.com",
                "code": "123456",
            }
        }


class UserForgotChangePassword(User):
    code: str
    newPassword: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "test@gmail.com",
                "code": "123456",
                "newPassword": "Hola111?",
            }
        }
