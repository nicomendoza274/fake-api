from pydantic.json_schema import SkipJsonSchema
from sqlalchemy import BigInteger
from sqlmodel import Field

from core.models.base import BaseAudit
from core.models.camel import Camel


class UserRoleBase(Camel):
    user_role_id: int | None = Field(sa_type=BigInteger, default=None, primary_key=True)
    user_id: int | None = Field(
        foreign_key="users.user_id",
        nullable=True,
        sa_type=BigInteger,
    )
    role_id: int | None = Field(
        foreign_key="roles.role_id",
        nullable=True,
        sa_type=BigInteger,
    )


class UserRole(UserRoleBase, BaseAudit, table=True):
    __tablename__: str = "user_roles"
    pass


class UserRoleResponseDTO(UserRoleBase):
    pass


class UserRoleDTO(UserRoleBase):
    user_role_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
