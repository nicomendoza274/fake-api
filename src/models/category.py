import sqlalchemy as sa
from pydantic import Field
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import BigInteger, Field

from src.core.models.base import BaseAudit
from src.core.models.camel import Camel


class CategoryBase(Camel):
    category_id: int | None = Field(sa_type=BigInteger, default=None, primary_key=True)
    name: str = Field(sa_column=sa.Column(sa.String, nullable=False))


class Category(CategoryBase, BaseAudit, table=True):
    __tablename__: str = "categories"
    pass


class CategoryResponseDTO(CategoryBase):
    pass


class CategoryDTO(CategoryBase):
    category_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
