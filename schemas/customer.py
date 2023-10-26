from datetime import datetime
from typing import Optional

from schemas.camel import CamelModel


class Customer(CamelModel):
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
        json_schema_extra = {
            "example": {
                "customerId": 0,
                "name": "Nombre",
                "internalId": "ASD123456",
                "address": "Caseros 123",
                "city": "Salta",
                "phone": "3875123456",
            }
        }
