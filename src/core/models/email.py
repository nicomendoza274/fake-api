from pydantic import BaseModel


class EmailMessage(BaseModel):
    full_name: str
    code: int
