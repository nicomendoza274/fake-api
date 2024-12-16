from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from core.schemas.camel import CamelModel


class CategoryBase(CamelModel):
    name: str
    internal_id: str
    address: str
    city: str
    phone: str

    class Config:
        from_attributes = True


class CustomerResponseDTO(CategoryBase):
    customer_id: int


class CustomerDTO(CategoryBase):
    customer_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
