from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    hash: Mapped[str] = mapped_column(String, nullable=False)
