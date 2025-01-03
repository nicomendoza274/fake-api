from pydantic import Field
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import BigInteger, Field

from core.models.base import BaseAudit
from core.models.camel import Camel


class CategoryBase(Camel):
    name: str = Field()


class Category(CategoryBase, BaseAudit, table=True):
    __tablename__ = "categories"  # type: ignore
    category_id: int | None = Field(sa_type=BigInteger, default=None, primary_key=True)


class CategoryResponseDTO(CategoryBase):
    category_id: int


class CategoryDTO(CategoryBase):
    category_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
