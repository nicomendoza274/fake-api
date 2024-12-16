from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from core.schemas.camel import CamelModel


class RoleBase(CamelModel):
    name: str

    class Config:
        from_attributes = True


class RoleResponseDTO(RoleBase):
    role_id: int


class RoleDTO(RoleBase):
    role_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
