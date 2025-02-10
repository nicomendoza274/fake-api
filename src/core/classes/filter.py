from dataclasses import dataclass
from typing import Type, TypeVar

import humps
from sqlmodel.sql.expression import SelectOfScalar

from core.enums.filter_criteria import FilterCriteriaEnum
from core.models.base import BaseAudit
from core.models.query import PropertyModel, QueryCriteria
from core.utils.query import get_property_values

T = TypeVar("T", bound=BaseAudit)


@dataclass
class FilterCriteria:

    def validate(
        self,
        result: SelectOfScalar[T],
        property_model_list: list[PropertyModel],
        sql_model: Type[T],
        query_criteria: QueryCriteria | None,
    ):
        if not query_criteria or not query_criteria.filters:
            return result

        filters = []
        for filter in query_criteria.filters:
            property_name = humps.decamelize(filter.property_name)
            first_properties, last_property = get_property_values(property_name)

            type_filter = filter.type
            value_filter = filter.value
            from_filter = filter.From
            to_filter = filter.To

            model = next(
                (
                    row.model
                    for row in property_model_list
                    if row.property == first_properties
                ),
                sql_model,
            )

            model_property = getattr(model, last_property)
            filter_criteria = {
                FilterCriteriaEnum.EQ.value: model_property == value_filter,
                FilterCriteriaEnum.NEQ.value: model_property != value_filter,
                FilterCriteriaEnum.GT.value: (
                    model_property > value_filter if value_filter else None
                ),
                FilterCriteriaEnum.LT.value: (
                    model_property < value_filter if value_filter else None
                ),
                FilterCriteriaEnum.GTE.value: (
                    model_property >= value_filter if value_filter else None
                ),
                FilterCriteriaEnum.LTE.value: (
                    model_property <= value_filter if value_filter else None
                ),
                FilterCriteriaEnum.BETWEEN.value: (
                    model_property.between(from_filter, to_filter)
                    if from_filter and to_filter
                    else None
                ),
                FilterCriteriaEnum.LIKE.value: model_property.like(f"%{value_filter}%"),
                FilterCriteriaEnum.CONTAINS.value: model_property.like(
                    f"%{value_filter}%"
                ),
            }

            filter_criteria = filter_criteria.get(type_filter, None)

            filters.append(filter_criteria)

        result = result.where(*filters)
        return result
