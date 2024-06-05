import json

import humps

from core.classes.generic_errors import GenericError
from core.constants.generic_errors import GEN_1000
from core.schemas.query import QueryCriteria
from core.utils.encrypt import base64_decode


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
    except:
        raise GenericError(GEN_1000)
    return query_criteria
