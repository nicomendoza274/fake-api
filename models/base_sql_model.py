from sqlalchemy import Column, DateTime, Integer, func


class BaseSqlModel:
    created_at = Column(DateTime(timezone=True), default=func.now())
    created_by = Column(Integer)
    updated_at = Column(DateTime(timezone=True))
    updated_by = Column(Integer)
    deleted_at = Column(DateTime(timezone=True))
    deleted_by = Column(Integer)
