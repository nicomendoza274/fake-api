from core.schemas.audit_schema import AuditSchema
from core.schemas.camel import CamelModel


class RoleBaseSchema(CamelModel):
    role_id: int | None
    name: str

    class Config:
        from_attributes = True


class RoleResponseDTO(RoleBaseSchema, AuditSchema):
    pass


class RoleDTO(RoleBaseSchema):
    role_id: int | None = None
