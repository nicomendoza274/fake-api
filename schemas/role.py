from schemas.base_schema import BaseSchema
from schemas.camel import CamelModel


class RoleBase(CamelModel):
    role_id: int | None
    name: str


class Role(RoleBase, BaseSchema):
    class Config:
        json_schema_extra = {"example": {"role_id": 0, "name": "Nombre"}}


class RoleUpdate(RoleBase):
    pass
