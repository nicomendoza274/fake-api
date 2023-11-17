from typing import List

from pydantic import BaseModel


class ErrorDescription(BaseModel):
    Code: str
    Exception: str
    Message: str


class Errors(BaseModel):
    Errors: List[ErrorDescription]
