from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from sqlmodel.sql.expression import SelectOfScalar

from src.core.classes.filter import FilterCriteria
from src.core.classes.search import SearchCriteria
from src.core.classes.sort import SortCriteria
from src.core.models.base import BaseAudit
from src.core.models.query import PropertyModel, QueryCriteria

T = TypeVar("T", bound=BaseAudit)


@dataclass
class QueryCriterionService(Generic[T]):
    filer_criteria = FilterCriteria()
    sort_criteria = SortCriteria()
    search_criteria = SearchCriteria()

    def validate_query(
        self,
        query_criteria: QueryCriteria | None,
        result: SelectOfScalar[T],
        property_model_list: list[PropertyModel],
        sql_model: Type[T],
        property_search: list,
    ):
        result = self.filer_criteria.validate(
            result,
            property_model_list,
            sql_model,
            query_criteria,
        )
        result = self.sort_criteria.validate(result, property_search, query_criteria)
        result = self.search_criteria.validate(
            result,
            property_model_list,
            query_criteria,
            sql_model,
        )
        return result
