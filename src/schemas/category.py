from core.schemas.audit_schema import AuditSchema
from core.schemas.camel import CamelModel


class CategoryBaseSchema(CamelModel):
    category_id: int | None
    name: str


class CategoryResponseDTO(CategoryBaseSchema, AuditSchema):

    class Config:
        from_attributes = True


class CategoryDTO(CategoryBaseSchema):
    category_id: int | None = None

    class Config:
        from_attributes = True
