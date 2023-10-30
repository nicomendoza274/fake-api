from schemas.base_schema import BaseSchema
from schemas.camel import CamelModel


class Product(CamelModel, BaseSchema):
    product_id: int
    name: str
    price: float

    class Config:
        json_schema_extra = {
            "example": {"product_id": 0, "name": "Nombre", "price": 1999.5}
        }


class ProductUpdate(CamelModel):
    product_id: int
    name: str
    price: float
