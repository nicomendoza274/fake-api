from sqlalchemy import Column, ForeignKey, Integer, String

from config.database import Base
from models.base_sql_model import BaseSqlModel


class UserCode(Base, BaseSqlModel):
    __tablename__ = "user_codes"

    user_code_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    code = Column(String)
