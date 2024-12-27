from pydantic import BaseModel


class EmailMessage(BaseModel):
    fullName: str
    code: int
