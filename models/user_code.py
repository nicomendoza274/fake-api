from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base
from models.base_sql_model import BaseSqlModel


class UserCode(Base, BaseSqlModel):
    __tablename__ = "user_codes"

    user_code_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id"), nullable=True
    )
    code: Mapped[str] = mapped_column(String)
