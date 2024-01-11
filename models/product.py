from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base
from models.base_sql_model import BaseSqlModel


class Product(Base, BaseSqlModel):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.category_id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean)
