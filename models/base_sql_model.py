from sqlalchemy import Column, DateTime, ForeignKey, Integer, func


class BaseSqlModel:
    created_at = Column(DateTime(timezone=True), default=func.now())
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    updated_at = Column(DateTime(timezone=True))
    updated_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    deleted_at = Column(DateTime(timezone=True))
    deleted_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
