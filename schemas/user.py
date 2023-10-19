from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    email: str
    password: str
class UserCreateModel(BaseModel):
    user_id: int
    email: str
    hash: str