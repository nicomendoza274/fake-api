from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column


class BaseSqlModel:
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    created_by: Mapped[DateTime] = mapped_column(
        Integer, ForeignKey("users.user_id"), nullable=True
    )
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    updated_by: Mapped[DateTime] = mapped_column(
        Integer, ForeignKey("users.user_id"), nullable=True
    )
    deleted_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    deleted_by: Mapped[DateTime] = mapped_column(
        Integer, ForeignKey("users.user_id"), nullable=True
    )
