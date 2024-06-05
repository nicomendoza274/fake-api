from typing import List

from pydantic import BaseModel


class Error(BaseModel):
    Code: str
    Exception: str
    Message: str
    Status: int | None = None


class Errors(BaseModel):
    Errors: List[Error]
