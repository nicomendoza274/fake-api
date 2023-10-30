from sqlalchemy import Column, Float, Integer, String

from config.database import Base
from models.base_sql_model import BaseSqlModel


class Product(Base, BaseSqlModel):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
