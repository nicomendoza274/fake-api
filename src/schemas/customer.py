from core.schemas.audit_schema import AuditSchema
from core.schemas.camel import CamelModel


class CategoryBaseSchema(CamelModel):
    customer_id: int | None
    name: str
    internal_id: str
    address: str
    city: str
    phone: str


class CustomerResponseDTO(CategoryBaseSchema, AuditSchema):

    class Config:
        from_attributes = True


class CustomerDTO(CategoryBaseSchema):
    customer_id: int | None = None
