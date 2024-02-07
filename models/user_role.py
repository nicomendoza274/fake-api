from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base
from models.base_sql_model import BaseSqlModel


class UserRole(Base, BaseSqlModel):
    __tablename__ = "user_roles"

    user_role_id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.role_id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=True)
