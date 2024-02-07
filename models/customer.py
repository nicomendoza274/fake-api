from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base
from models.base_sql_model import BaseSqlModel


class Customer(Base, BaseSqlModel):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    internal_id: Mapped[str]
    address: Mapped[str]
    city: Mapped[str]
    phone: Mapped[str]
