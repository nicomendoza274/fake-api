from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column


class BaseSqlModel:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    created_by: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_by: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_by: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=True)
