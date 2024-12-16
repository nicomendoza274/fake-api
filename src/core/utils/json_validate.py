from typing import Type, TypeVar

from fastapi import status
from pydantic import ValidationError

from core.classes.handle_exception import HandleException
from core.constants.generic_errors import GEN_1002
from core.schemas.camel import CamelModel

T = TypeVar("T", bound=CamelModel)


def validate_json_data(model: Type[T], json_data: str) -> T:
    try:
        return model.model_validate_json(json_data)
    except ValidationError:
        raise HandleException([GEN_1002], status.HTTP_400_BAD_REQUEST)
