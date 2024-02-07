from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base
from models.base_sql_model import BaseSqlModel


class Role(Base, BaseSqlModel):
    __tablename__ = "roles"

    role_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
