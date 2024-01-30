from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    hash: Mapped[str]
