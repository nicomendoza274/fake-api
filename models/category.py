from sqlalchemy import Column, Integer, String

from config.database import Base
from models.base_sql_model import BaseSqlModel


class Category(Base, BaseSqlModel):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True)
    name = Column(String)
