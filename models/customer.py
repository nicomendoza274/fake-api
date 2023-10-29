from sqlalchemy import Column, Integer, String

from config.database import Base
from models.base_sql_model import BaseSqlModel


class Customer(Base, BaseSqlModel):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    name = Column(String)
    internal_id = Column(String)
    address = Column(String)
    city = Column(String)
    phone = Column(String)
