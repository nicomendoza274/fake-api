from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key= True)
    email = Column(String)
    hash = Column(String, nullable=False)
    # created_at = Column(DateTime)
    # created_by = Column(Integer)
    # updated_at = Column(DateTime)
    # updated_by = Column(Integer)
    # deleted_at = Column(DateTime)
    # deleted_by = Column(Integer)
