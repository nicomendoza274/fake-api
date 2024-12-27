from pydantic import BaseModel, Field


class Error(BaseModel):
    Code: str
    Exception: str
    Message: str
    Status: int = Field(..., exclude=True)


class Errors(BaseModel):
    Errors: list[Error]
