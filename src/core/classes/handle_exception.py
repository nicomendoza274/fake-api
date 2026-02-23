from dataclasses import dataclass
from typing import List

from fastapi import status

from src.core.models.error import Error


@dataclass
class HandleException(Exception):
    errors: List[Error]
    status_code: int = status.HTTP_400_BAD_REQUEST
