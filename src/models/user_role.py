from pydantic.json_schema import SkipJsonSchema
from sqlalchemy import BigInteger
from sqlmodel import Field

from core.models.base import BaseAuditModel
from core.models.camel import CamelModel


class UserRoleBase(CamelModel):
    user_id: int = Field(foreign_key="users.user_id", nullable=True)
    role_id: int = Field(foreign_key="roles.role_id", nullable=True)


class UserRole(UserRoleBase, BaseAuditModel, table=True):
    __tablename__ = "user_roles"  # type: ignore
    user_role_id: int = Field(sa_type=BigInteger, primary_key=True)


class UserRoleResponseDTO(UserRoleBase):
    user_role_id: int | None


class UserRoleDTO(UserRoleBase):
    user_role_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
