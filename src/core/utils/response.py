from typing import List, TypeVar

from fastapi import Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core.models.camel import Camel
from core.models.error import Error, Errors
from core.models.response import MultipleResponseData, ResponseData

T = TypeVar("T", bound=Camel)


def get_empty_response(status_code: int = status.HTTP_200_OK) -> Response:
    return Response(status_code=status_code)


def get_response(
    data: List[T] | T, status_code: int = status.HTTP_200_OK
) -> JSONResponse:
    response = jsonable_encoder(ResponseData(data=data))
    return JSONResponse(content=response, status_code=status_code)


def get_multiple_response(
    count: int,
    start: int | None,
    length: int | None,
    data: List[T] | T,
    status_code: int = status.HTTP_200_OK,
) -> JSONResponse:
    response = jsonable_encoder(
        MultipleResponseData(
            count=count,
            start=start,
            length=length,
            data=data,
        )
    )
    return JSONResponse(
        content=response,
        status_code=status_code,
    )


def get_error_response(
    errors: List[Error],
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> JSONResponse:
    errors_data = Errors(Errors=errors)
    content = errors_data.model_dump()
    return JSONResponse(content=content, status_code=status_code)
