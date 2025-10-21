import sqlalchemy as sa
from pydantic import Field
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import BigInteger, Field

from core.models.base import BaseAudit
from core.models.camel import Camel


class CategoryBase(Camel):
    customer_id: int | None = Field(sa_type=BigInteger, default=None, primary_key=True)
    name: str = Field(sa_column=sa.Column(sa.String, nullable=False))
    internal_id: str = Field(sa_column=sa.Column(sa.String, nullable=False))
    address: str = Field(sa_column=sa.Column(sa.String, nullable=False))
    city: str = Field(sa_column=sa.Column(sa.String, nullable=False))
    phone: str = Field(sa_column=sa.Column(sa.String, nullable=False))


class Customer(CategoryBase, BaseAudit, table=True):
    __tablename__: str = "customers"
    pass


class CustomerResponseDTO(CategoryBase):
    pass


class CustomerDTO(CategoryBase):
    customer_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
