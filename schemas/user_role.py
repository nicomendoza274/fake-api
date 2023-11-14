from typing import Optional

from schemas.base_schema import BaseSchema
from schemas.camel import CamelModel


class UserRoleBase(CamelModel):
    user_role_id: int
    role_id: int
    user_id: int


class UserRole(UserRoleBase, BaseSchema):
    class Config:
        json_schema_extra = {"example": {"user_role_id": 0, "role_id": 0, "user_id": 0}}


class UserRoleUpdate(UserRoleBase):
    pass
