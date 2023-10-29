from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseSchema(BaseModel):
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = None
