from core.schemas.audit_schema import AuditSchema
from core.schemas.camel import CamelModel


class RoleBaseSchema(CamelModel):
    role_id: int | None
    name: str


class RoleResponseDTO(RoleBaseSchema, AuditSchema):
    class Config:
        from_attributes = True


class RoleDTO(RoleBaseSchema):
    role_id: int | None = None

    class Config:
        from_attributes = True
