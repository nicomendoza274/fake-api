from schemas.base_schema import BaseSchema
from schemas.camel import CamelModel


class Category(CamelModel, BaseSchema):
    category_id: int
    name: str

    class Config:
        json_schema_extra = {"example": {"category_id": 0, "name": "Nombre"}}


class CategoryUpdate(CamelModel):
    category_id: int
    name: str
