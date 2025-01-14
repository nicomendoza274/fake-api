from fastapi import Form, UploadFile
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import BigInteger, Field, Relationship, and_

from core.models.base import BaseAudit
from core.models.camel import Camel
from core.models.file import File, FileDTO
from models.category import Category, CategoryDTO


class ProductBase(Camel):
    name: str = Field()
    price: float = Field()
    is_active: bool = Field()

    # Foreign keys
    category_id: int | None = Field(
        default=None, foreign_key="categories.category_id", nullable=True
    )
    picture_id: int | None = Field(
        default=None, foreign_key="files.file_id", nullable=True
    )


class Product(ProductBase, BaseAudit, table=True):
    __tablename__: str = "products"

    product_id: int | None = Field(sa_type=BigInteger, default=None, primary_key=True)

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
    product_id: int
    category: CategoryDTO | None
    picture: FileDTO | None = None


class ProductDTO(ProductBase):
    product_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)


class CreateProductDTO(Camel):
    data: str = Form(...)
    picture: UploadFile | None = None
