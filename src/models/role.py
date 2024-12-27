from pydantic import Field
from pydantic.json_schema import SkipJsonSchema
from sqlalchemy import BigInteger
from sqlmodel import Field

from core.models.base import BaseAuditModel
from core.models.camel import CamelModel


class RoleBase(CamelModel):
    name: str = Field()


class Role(RoleBase, BaseAuditModel, table=True):
    __tablename__ = "roles"  # type: ignore
    role_id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)


class RoleResponseDTO(RoleBase):
    role_id: int


class RoleDTO(RoleBase):
    role_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
