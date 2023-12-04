from sqlalchemy import Column, ForeignKey, Integer

from config.database import Base
from models.base_sql_model import BaseSqlModel


class UserRole(Base, BaseSqlModel):
    __tablename__ = "user_roles"

    user_role_id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
