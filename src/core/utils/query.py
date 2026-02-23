import json

import humps
from fastapi import status

from src.core.classes.handle_exception import HandleException
from src.core.constants.generic_errors import GEN_1000
from src.core.models.query import QueryCriteria
from src.core.utils.encrypt import base64_decode


def str_to_dict(query: str) -> dict:
    query_decode = base64_decode(query)
    query_dict_camel = json.loads(query_decode)
    query_dict_snake = humps.decamelize(query_dict_camel)
    query_dict = {key.lower(): value for key, value in query_dict_snake.items()}

    return query_dict


def str_to_query(query: str | None) -> QueryCriteria | None:
    if not query:
        return None

    try:
        query_dict = str_to_dict(query)
        query_criteria = QueryCriteria.model_validate(query_dict)
    except ValueError:
        raise HandleException([GEN_1000], status.HTTP_400_BAD_REQUEST)
    return query_criteria


def get_property_values(property_name: str) -> tuple[str, str]:
    if "." not in property_name:
        return "", property_name

    first_properties, last_property = property_name.rsplit(".", 1)
    return first_properties, last_property
