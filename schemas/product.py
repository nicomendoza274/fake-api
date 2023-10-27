from datetime import datetime
from typing import Optional

from schemas.camel import CamelModel


class Product(CamelModel):
    product_id: int
    name: str
    price: float
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {"product_id": 0, "name": "Nombre", "price": 1999.5}
        }
