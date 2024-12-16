from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from core.schemas.camel import CamelModel
from core.schemas.file import FileDTO
from schemas.category import CategoryDTO


class ProductBase(CamelModel):
    category_id: int | None
    name: str
    price: float
    is_active: bool
    file_id: int | None = None

    class Config:
        from_attributes = True


class ProductResponseDTO(ProductBase):
    product_id: int
    category: CategoryDTO | None
    picture: FileDTO | None = None


class ProductDTO(ProductBase):
    product_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
