from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base
from models.base_sql_model import BaseSqlModel


class Product(Base, BaseSqlModel):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.category_id"), nullable=True
    )
    name: Mapped[str]
    price: Mapped[float]
    is_active: Mapped[bool]
