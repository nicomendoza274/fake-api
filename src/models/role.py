import sqlalchemy as sa
from pydantic import Field
from pydantic.json_schema import SkipJsonSchema
from sqlalchemy import BigInteger
from sqlmodel import Field

from src.core.models.base import BaseAudit
from src.core.models.camel import Camel


class RoleBase(Camel):
    role_id: int | None = Field(sa_type=BigInteger, default=None, primary_key=True)
    name: str = Field(sa_column=sa.Column(sa.String, nullable=False))


class Role(RoleBase, BaseAudit, table=True):
    __tablename__: str = "roles"
    pass


class RoleResponseDTO(RoleBase):
    pass


class RoleDTO(RoleBase):
    role_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
