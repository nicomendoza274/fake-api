import humps
from sqlmodel import desc, or_

from core.enums.filter_criteria import FilterCriteriaEnum
from core.models.query import PropertyModel, QueryCriteria
from core.utils.query import get_property_values


class QueryCriterionService:

    def __init__(self, sql_model, query_criteria: QueryCriteria | None) -> None:
        self.sql_model = sql_model
        self.query_criteria = query_criteria

    def filters(self, result, property_model_list: list[PropertyModel]):
        if not self.query_criteria or not self.query_criteria.filters:
            return result

        filters = []
        for filter in self.query_criteria.filters:
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
                self.sql_model,
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

    def search(self, result, property_search: list):
        if not self.query_criteria or not self.query_criteria.search:
            return result

        search = f"%{self.query_criteria.search}%"

        filters = [prop.ilike(search) for prop in property_search]

        result = result.where(or_(*filters))
        return result

    def sorts(self, result, property_model_list: list[PropertyModel]):
        if not self.query_criteria or not self.query_criteria.sorts:
            return result

        clauses = []
        for sort in self.query_criteria.sorts:
            property_name = humps.decamelize(sort.property_name)
            first_properties, last_property = get_property_values(property_name)

            model = next(
                (
                    row.model
                    for row in property_model_list
                    if row.property == first_properties
                ),
                self.sql_model,
            )

            clause = (
                getattr(model, last_property)
                if not sort.descending
                else desc(getattr(model, last_property))
            )
            clauses.append(clause)

        result = result.order_by(*clauses)

        return result
