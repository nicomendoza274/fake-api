from typing import Any, List

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
    sorts: List[SortCriteria] | None = None
    filters: List[FilterCriteria] | None = None
    search: str | None = None
