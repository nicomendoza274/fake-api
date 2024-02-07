from typing import List, Optional

from fastapi import Query

from schemas.base_schema import BaseSchema
from schemas.camel import CamelModel
from schemas.category import CategoryUpdate


class ProductBase(CamelModel):
    product_id: int | None
    category_id: Optional[int]
    name: str
    price: float
    is_active: bool


class Product(ProductBase, BaseSchema):
    class Config:
        json_schema_extra = {
            "example": {"product_id": 0, "name": "Benjamin Lopez", "price": 1999.5}
        }


class ProductUpdate(ProductBase):
    pass


class ProductCategory(ProductBase, BaseSchema):
    category: Optional[CategoryUpdate]


class ProductActiveToggle(CamelModel):
    is_active: bool


class ProductDelteMultiple(CamelModel):
    ids: List[int] = Query(...)
