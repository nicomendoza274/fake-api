from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Customer(BaseModel):
    customer_id: Optional[int] = None
    name: str
    internal_id: str
    address: str
    city: str
    phone: str
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "customer_id": 0,
                "name": "Nombre",
                "internal_id": "ASD123456",
                "address": "Caseros 123",
                "city": "Salta",
                "phone": "3875123456"
            }
        }
