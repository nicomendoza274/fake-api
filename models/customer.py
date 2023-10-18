from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key= True)
    name = Column(String)
    internal_id = Column(String)
    address = Column(String)
    city = Column(String)
    phone = Column(String)
    created_at = Column(DateTime)
    created_by = Column(Integer)
    updated_at = Column(DateTime)
    updated_by = Column(Integer)
    deleted_at = Column(DateTime)
    deleted_by = Column(Integer)
