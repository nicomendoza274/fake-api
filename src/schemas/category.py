from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from core.schemas.camel import CamelModel


class CategoryBase(CamelModel):
    name: str

    class Config:
        from_attributes = True


class CategoryResponseDTO(CategoryBase):
    category_id: int


class CategoryDTO(CategoryBase):
    category_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
