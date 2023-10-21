from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Customer(BaseModel):
    customer_id: Optional[int] = None
    name: str
    internal_id: str
    address: str
    city: str
    phone: str
    created_at: Optional[datetime]
    created_by: Optional[int]
    updated_at: Optional[datetime]
    updated_by: Optional[int]
    deleted_at: Optional[datetime]
    deleted_by: Optional[int]

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": 0,
                "name": "Nombre",
                "internal_id": "ASD123456",
                "address": "Caseros 123",
                "city": "Salta",
                "phone": "3875123456",
            }
        }
