from schemas.base_schema import BaseSchema
from schemas.camel import CamelModel


class CategoryBase(CamelModel):
    customer_id: int | None
    name: str
    internal_id: str
    address: str
    city: str
    phone: str


class Customer(CategoryBase, BaseSchema):
    pass

    class Config:
        json_schema_extra = {
            "example": {
                "customerId": 0,
                "name": "Nombre",
                "internalId": "ASD123456",
                "address": "Caseros 123",
                "city": "Salta",
                "phone": "3875123456",
            }
        }


class CustomerUpdate(CategoryBase):
    pass
