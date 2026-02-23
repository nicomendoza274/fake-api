from dataclasses import dataclass
from typing import TypeVar

from sqlmodel import or_

from src.core.models.base import BaseAudit
from src.core.models.query import QueryCriteria

T = TypeVar("T", bound=BaseAudit)


@dataclass
class SortCriteria:
    def validate(
        self,
        result,
        property_search: list,
        query_criteria: QueryCriteria | None,
    ):
        if not query_criteria or not query_criteria.search:
            return result

        search = f"%{query_criteria.search}%"

        filters = [prop.ilike(search) for prop in property_search]

        result = result.where(or_(*filters))
        return result
