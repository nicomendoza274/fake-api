from typing import Optional

from schemas.camel import CamelModel


class User(CamelModel):
    email: str


class UserLogin(User):
    password: str


class UserCreate(User):
    user_id: int
    hash: str


class UserLoged(User):
    user_id: int
    token: str
