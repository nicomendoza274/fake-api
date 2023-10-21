from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str


class UserCreateModel(BaseModel):
    user_id: int
    email: str
    hash: str
