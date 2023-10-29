from sqlalchemy import Column, DateTime, Float, Integer, String, func

from config.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    created_at = Column(DateTime(timezone=True), default=func.now())
    created_by = Column(Integer)
    updated_at = Column(DateTime(timezone=True))
    updated_by = Column(Integer)
    deleted_at = Column(DateTime(timezone=True))
    deleted_by = Column(Integer)
