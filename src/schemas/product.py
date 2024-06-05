from typing import List

from fastapi import Query

from core.schemas.audit_schema import AuditSchema
from core.schemas.camel import CamelModel
from schemas.category import CategoryDTO, CategoryResponseDTO


class ProductBaseSchema(CamelModel):
    product_id: int | None
    category_id: int | None
    name: str
    price: float
    is_active: bool


class ProductResponseDTO(ProductBaseSchema, AuditSchema):
    category: CategoryDTO | None

    class Config:
        from_attributes = True


class ProductDTO(ProductBaseSchema):
    product_id: int | None = None


class ProductActiveToggleDTO(CamelModel):
    is_active: bool
