from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from core.schemas.camel import CamelModel


class UserRoleBase(CamelModel):
    role_id: int
    user_id: int

    class Config:
        from_attributes = True


class UserRoleResponseDTO(UserRoleBase):
    user_role_id: int | None


class UserRoleDTO(UserRoleBase):
    user_role_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
