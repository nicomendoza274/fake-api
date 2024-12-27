from pydantic import Field
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import Field

from core.models.base import BaseAuditModel
from core.models.camel import CamelModel


class CategoryBase(CamelModel):
    name: str = Field()


class Category(CategoryBase, BaseAuditModel, table=True):
    __tablename__ = "categories"  # type: ignore
    category_id: int | None = Field(default=None, primary_key=True)


class CategoryResponseDTO(CategoryBase):
    category_id: int


class CategoryDTO(CategoryBase):
    category_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
