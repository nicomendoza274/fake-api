from pydantic import Field
from pydantic.json_schema import SkipJsonSchema
from sqlalchemy import BigInteger
from sqlmodel import Field

from core.models.base import BaseAudit
from core.models.camel import Camel


class RoleBase(Camel):
    name: str = Field()


class Role(RoleBase, BaseAudit, table=True):
    __tablename__: str = "roles"
    role_id: int | None = Field(sa_type=BigInteger, default=None, primary_key=True)


class RoleResponseDTO(RoleBase):
    role_id: int


class RoleDTO(RoleBase):
    role_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
