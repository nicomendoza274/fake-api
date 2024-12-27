from typing import List

from fastapi import status

from core.models.error import Error


class HandleException(Exception):

    def __init__(
        self,
        errors: List[Error],
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        self.errors = errors
        self.status_code = status_code
