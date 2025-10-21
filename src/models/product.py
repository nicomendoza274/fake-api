from decimal import Decimal

import sqlalchemy as sa
from fastapi import Form, UploadFile
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import BigInteger, Field, Relationship, and_

from core.models.base import BaseAudit
from core.models.camel import Camel
from core.models.file import File, FileDTO
from models.category import Category, CategoryDTO


class ProductBase(Camel):
    product_id: int | None = Field(sa_type=BigInteger, default=None, primary_key=True)
    name: str = Field(sa_column=sa.Column(sa.String, nullable=False))
    price: Decimal = Field(
        sa_column=sa.Column(sa.Numeric(10, 2), nullable=False), default=Decimal("0.00")
    )
    is_active: bool = Field()

    # Foreign keys
    category_id: int | None = Field(
        default=None,
        foreign_key="categories.category_id",
        nullable=True,
        sa_type=BigInteger,
    )
    picture_id: int | None = Field(
        default=None,
        foreign_key="files.file_id",
        nullable=True,
        sa_type=BigInteger,
    )


class Product(ProductBase, BaseAudit, table=True):
    __tablename__: str = "products"

    # Relationships
    picture: File | None = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": lambda: and_(
                File.file_id == Product.picture_id,
                File.deleted_at == None,
            )
        }
    )

    category: Category | None = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": lambda: and_(
                Category.category_id == Product.category_id,
                Category.deleted_at == None,
            )
        }
    )


class ProductResponseDTO(ProductBase):
    category: CategoryDTO | None
    picture: FileDTO | None = None


class ProductDTO(ProductBase):
    product_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)


class CreateProductDTO(Camel):
    data: str = Form(...)
    picture: UploadFile | None = None
