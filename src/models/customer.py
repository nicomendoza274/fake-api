from pydantic import Field
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import BigInteger, Field

from core.models.base import BaseAudit
from core.models.camel import Camel


class CategoryBase(Camel):
    name: str = Field()
    internal_id: str = Field()
    address: str = Field()
    city: str = Field()
    phone: str = Field()


class Customer(CategoryBase, BaseAudit, table=True):
    __tablename__: str = "customers"
    customer_id: int | None = Field(sa_type=BigInteger, default=None, primary_key=True)


class CustomerResponseDTO(CategoryBase):
    customer_id: int


class CustomerDTO(CategoryBase):
    customer_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)
