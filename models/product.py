from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String

from config.database import Base
from models.base_sql_model import BaseSqlModel


class Product(Base, BaseSqlModel):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=True)
    name = Column(String)
    price = Column(Float)
    is_active = Column(Boolean)
