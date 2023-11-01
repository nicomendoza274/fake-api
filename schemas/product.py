from typing import Optional

from schemas.base_schema import BaseSchema
from schemas.camel import CamelModel
from schemas.category import CategoryUpdate


class Product(CamelModel, BaseSchema):
    product_id: int
    category_id: Optional[int]
    name: str
    price: float

    class Config:
        json_schema_extra = {
            "example": {"product_id": 0, "name": "Nombre", "price": 1999.5}
        }


class ProductUpdate(CamelModel):
    product_id: int
    category_id: Optional[int]
    name: str
    price: float


class ProductCategory(CamelModel, BaseSchema):
    product_id: int
    category_id: Optional[int]
    name: str
    price: float
    category: Optional[CategoryUpdate]
