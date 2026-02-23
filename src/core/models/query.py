from typing import Any

from src.core.models.camel import Camel


class SortCriteria(Camel):
    property_name: str
    descending: bool


class FilterCriteria(Camel):
    property_name: str
    type: str
    value: Any = None
    From: Any = None
    To: Any = None


class QueryCriteria(Camel):
    sorts: list[SortCriteria] | None = None
    filters: list[FilterCriteria] | None = None
    search: str | None = None


class PropertyModel(Camel):
    property: str
    model: Any
