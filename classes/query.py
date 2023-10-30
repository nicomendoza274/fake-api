from sqlalchemy import desc

from utils.snake_case import to_snake_case


class Query:
    def __init__(self, db_query, model) -> None:
        self.db_query = db_query
        self.model = model

    def sorts(self, json: dict):
        for sort in json["sorts"]:
            property_name = to_snake_case(sort["propertyName"])
            descending = sort["descending"]

            if descending == False:
                self.db_query = self.db_query.order_by(property_name)
            else:
                self.db_query = self.db_query.order_by(desc(property_name))
        return self.db_query

    def filters(self, json: dict):
        for filter in json["filters"]:
            property_name = to_snake_case(filter["propertyName"])
            type_filer = filter["type"]
            value_filter = filter["value"]

            if type_filer == "eq":
                self.db_query = self.db_query.filter(
                    getattr(self.model, property_name) == value_filter
                )
            elif type_filer == "neq":
                self.db_query = self.db_query.filter(
                    getattr(self.model, property_name) != value_filter
                )
            elif type_filer == "gt":
                self.db_query = self.db_query.filter(
                    getattr(self.model, property_name) > value_filter
                )
            elif type_filer == "lt":
                self.db_query = self.db_query.filter(
                    getattr(self.model, property_name) < value_filter
                )
            elif type_filer == "gte":
                self.db_query = self.db_query.filter(
                    getattr(self.model, property_name) >= value_filter
                )
            elif type_filer == "lte":
                self.db_query = self.db_query.filter(
                    getattr(self.model, property_name) <= value_filter
                )
            elif type_filer == "like":
                search = "%{}%".format(value_filter)
                self.db_query = self.db_query.filter(
                    getattr(self.model, property_name).like(search)
                )
            elif type_filer == "contains":
                search = "%{}%".format(value_filter)
                self.db_query = self.db_query.filter(
                    getattr(self.model, property_name).like(search)
                )
        return self.db_query

    def search(self, json: dict, value: str):
        search = json["search"]
        search = "%{}%".format(search)
        self.db_query = self.db_query.filter(getattr(self.model, value).ilike(search))
        return self.db_query
