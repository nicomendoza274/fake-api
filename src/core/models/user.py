from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class UserModel:
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    hash: Mapped[str]
