from sqlalchemy import Column, DateTime, Integer, String, func

from config.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    name = Column(String)
    internal_id = Column(String)
    address = Column(String)
    city = Column(String)
    phone = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    created_by = Column(Integer)
    updated_at = Column(DateTime(timezone=True))
    updated_by = Column(Integer)
    deleted_at = Column(DateTime(timezone=True))
    deleted_by = Column(Integer)
