from schemas.base_schema import BaseSchema
from schemas.camel import CamelModel


class CategoryBase(CamelModel):
    category_id: int | None
    name: str


class Category(CategoryBase, BaseSchema):
    class Config:
        json_schema_extra = {"example": {"category_id": 0, "name": "Nombre"}}


class CategoryUpdate(CategoryBase):
    pass
