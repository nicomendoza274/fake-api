from pydantic import BaseModel


class SuccessDTO(BaseModel):
    success: bool = True
