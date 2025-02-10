from dataclasses import dataclass
from typing import Type, TypeVar

import humps
from sqlmodel import desc

from core.models.base import BaseAudit
from core.models.query import PropertyModel, QueryCriteria
from core.utils.query import get_property_values

T = TypeVar("T", bound=BaseAudit)


@dataclass
class SearchCriteria:

    def validate(
        self,
        result,
        property_model_list: list[PropertyModel],
        query_criteria: QueryCriteria | None,
        sql_model: Type[T],
    ):
        if not query_criteria or not query_criteria.sorts:
            return result

        clauses = []
        for sort in query_criteria.sorts:
            property_name = humps.decamelize(sort.property_name)
            first_properties, last_property = get_property_values(property_name)

            model = next(
                (
                    row.model
                    for row in property_model_list
                    if row.property == first_properties
                ),
                sql_model,
            )

            clause = (
                getattr(model, last_property)
                if not sort.descending
                else desc(getattr(model, last_property))
            )
            clauses.append(clause)

        result = result.order_by(*clauses)
        return result
