from pydantic.json_schema import SkipJsonSchema
from sqlmodel import Field, Relationship, and_

from core.models.base import BaseAuditModel
from core.models.camel import CamelModel
from core.models.file import FileDTO, FileModel
from models.category import Category, CategoryDTO


class ProductBase(CamelModel):
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


class Product(ProductBase, BaseAuditModel, table=True):
    __tablename__ = "products"  # type: ignore

    product_id: int | None = Field(default=None, primary_key=True)

    # Relationships
    picture: FileModel | None = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": lambda: and_(
                FileModel.file_id == Product.picture_id,
                FileModel.deleted_at == None,
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
