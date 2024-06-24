from core.schemas.audit_schema import AuditSchema
from core.schemas.camel import CamelModel


class CategoryBaseSchema(CamelModel):
    category_id: int | None
    name: str

    class Config:
        from_attributes = True


class CategoryResponseDTO(CategoryBaseSchema, AuditSchema):
    pass


class CategoryDTO(CategoryBaseSchema):
    category_id: int | None = None
