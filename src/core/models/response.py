from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class MultipleResponseData(BaseModel, Generic[T]):
    count: int
    start: int | None
    length: int | None
    data: T


class ResponseData(BaseModel, Generic[T]):
    data: T
