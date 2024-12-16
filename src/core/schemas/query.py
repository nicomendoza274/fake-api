from typing import Any

from core.schemas.camel import CamelModel


class SortCriteria(CamelModel):
    property_name: str
    descending: bool


class FilterCriteria(CamelModel):
    property_name: str
    type: str
    value: Any = None
    From: Any = None
    To: Any = None


class QueryCriteria(CamelModel):
    sorts: list[SortCriteria] | None = None
    filters: list[FilterCriteria] | None = None
    search: str | None = None


class PropertyModel(CamelModel):
    property: str
    model: Any
