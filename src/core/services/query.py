from typing import List

import humps
from sqlalchemy import desc, or_
from sqlalchemy.orm.query import Query

from core.enums.filter_criteria import FilterCriteriaEnum
from core.schemas.query import PropertyModel
from core.utils.query import get_property_values, str_to_query


class QueryCriterionService:

    def __init__(self, sql_model, query: str | None) -> None:
        self.sql_model = sql_model
        self.query_criteria = str_to_query(query)

    def filters(self, result: Query, property_model_list: List[PropertyModel]) -> Query:
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

            filter_criteria = None
            model_property = getattr(model, last_property)
            if type_filter == FilterCriteriaEnum.EQ.value:
                filter_criteria = model_property == value_filter
            elif type_filter == FilterCriteriaEnum.NEQ.value:
                filter_criteria = model_property != value_filter
            elif type_filter == FilterCriteriaEnum.GT.value:
                filter_criteria = model_property > value_filter
            elif type_filter == FilterCriteriaEnum.LT.value:
                filter_criteria = model_property < value_filter
            elif type_filter == FilterCriteriaEnum.GTE.value:
                filter_criteria = model_property >= value_filter
            elif type_filter == FilterCriteriaEnum.LTE.value:
                filter_criteria = model_property <= value_filter
            elif (
                type_filter == FilterCriteriaEnum.BETWEEN.value
                and from_filter
                and to_filter
            ):
                filter_criteria = model_property.between(from_filter, to_filter)
            elif type_filter == FilterCriteriaEnum.LIKE.value:
                filter_criteria = model_property.like(f"%{value_filter}%")
            elif type_filter == FilterCriteriaEnum.CONTAINS.value:
                filter_criteria = model_property.like(f"%{value_filter}%")

            if filter_criteria:
                filters.append(filter_criteria)

        result = result.filter(*filters)

        return result

    def search(self, result: Query, property_search: List) -> Query:
        if not self.query_criteria or not self.query_criteria.search:
            return result

        search = f"%{self.query_criteria.search}%"

        filters = [prop.ilike(search) for prop in property_search]

        result = result.filter(or_(*filters))
        return result

    def sorts(self, result: Query, property_model_list: List[PropertyModel]) -> Query:
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
