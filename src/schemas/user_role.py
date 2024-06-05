from core.schemas.audit_schema import AuditSchema
from core.schemas.camel import CamelModel


class UserRoleBaseSchema(CamelModel):
    user_role_id: int | None
    role_id: int
    user_id: int


class UserRoleResponseDTO(UserRoleBaseSchema, AuditSchema):
    class Config:
        from_attributes = True


class UserRoleDTO(UserRoleBaseSchema):
    user_role_id: int | None = None

    class Config:
        from_attributes = True
