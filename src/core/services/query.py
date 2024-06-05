import humps
from sqlalchemy import desc

from core.enums.filter_criteria import FilterCriteriaEnum
from core.schemas.query import QueryCriteria


class QueryCriterionService:
    def __init__(self, sql_model) -> None:
        self.sql_model = sql_model

    def sorts(self, query_criteria: QueryCriteria | None, result):
        if not query_criteria or not query_criteria.sorts:
            return result

        for sort in query_criteria.sorts:
            property_name = humps.decamelize(sort.property_name)
            if sort.descending == False:
                result = result.order_by(property_name)
            else:
                result = result.order_by(desc(property_name))

        return result

    def filters(self, query_criteria: QueryCriteria | None, result):
        if not query_criteria or not query_criteria.filters:
            return result

        for filter in query_criteria.filters:
            property_name = humps.decamelize(filter.property_name)
            type_filer = filter.type
            value_filter = filter.value
            from_filter = filter.From
            to_filter = filter.To

            if type_filer == FilterCriteriaEnum.EQ.value:
                result = result.filter(
                    getattr(self.sql_model, property_name) == value_filter
                )
            elif type_filer == FilterCriteriaEnum.NEQ.value:
                result = result.filter(
                    getattr(self.sql_model, property_name) != value_filter
                )
            elif type_filer == FilterCriteriaEnum.GT.value:
                result = result.filter(
                    getattr(self.sql_model, property_name) > value_filter
                )
            elif type_filer == FilterCriteriaEnum.LT.value:
                result = result.filter(
                    getattr(self.sql_model, property_name) < value_filter
                )
            elif type_filer == FilterCriteriaEnum.GTE.value:
                result = result.filter(
                    getattr(self.sql_model, property_name) >= value_filter
                )
            elif type_filer == FilterCriteriaEnum.LTE.value:
                result = result.filter(
                    getattr(self.sql_model, property_name) <= value_filter
                )
            elif (
                type_filer == FilterCriteriaEnum.BETWEEN.value
                and from_filter
                and to_filter
            ):
                result = result.filter(
                    getattr(self.sql_model, property_name).between(
                        from_filter, to_filter
                    )
                )
            elif type_filer == FilterCriteriaEnum.LIKE.value:
                search = "%{}%".format(value_filter)
                result = result.filter(
                    getattr(self.sql_model, property_name).like(search)
                )
            elif type_filer == FilterCriteriaEnum.CONTAINS.value:
                search = "%{}%".format(value_filter)
                result = result.filter(
                    getattr(self.sql_model, property_name).like(search)
                )

        return result

    def search(self, query_criteria: QueryCriteria | None, property_name: str, result):
        if not query_criteria or not query_criteria.search:
            return result

        property_name = humps.decamelize(property_name)
        search = query_criteria.search
        search = "%{}%".format(search)
        result = result.filter(getattr(self.sql_model, property_name).ilike(search))
        return result
