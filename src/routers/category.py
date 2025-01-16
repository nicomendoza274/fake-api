from fastapi import APIRouter, Depends, Path, status

from core.constants.responses import NOT_200, NOT_201, NOT_422
from core.database.database import SessionDep
from core.models.response import MultipleResponseData, ResponseData
from core.utils.query import str_to_query
from core.utils.response import get_empty_response, get_multiple_response, get_response
from middlewares.jwt_bearer import JWTBearer
from models.category import CategoryDTO, CategoryResponseDTO
from models.user import User
from services.category import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get(
    path="",
    response_model=MultipleResponseData[CategoryResponseDTO],
    responses=NOT_422,
)
def list_data(
    session: SessionDep,
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    user: User = Depends(JWTBearer()),
):
    query_criteria = str_to_query(query)

    category_list, total_count = CategoryService(session, user).get_records(
        start, length, query_criteria
    )
    response = get_multiple_response(
        count=total_count,
        start=start,
        length=len(category_list) if length == 0 else length,
        data=category_list,
    )
    return response


@router.get(
    path="/{categoryId}",
    response_model=ResponseData[CategoryResponseDTO],
    responses=NOT_422,
)
def get_data(
    session: SessionDep,
    category_id: int = Path(alias="categoryId"),
    user: User = Depends(JWTBearer()),
):
    category_data = CategoryService(session, user).get_record(category_id)
    response = get_response(category_data)
    return response


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    responses=NOT_422 | NOT_201,
)
def create_data(
    category: CategoryDTO,
    session: SessionDep,
    user: User = Depends(JWTBearer()),
):
    CategoryService(session, user).create_record(category)
    response = get_empty_response(status.HTTP_201_CREATED)
    return response


@router.put(
    path="/{categoryId}",
    response_model=None,
    responses=NOT_422 | NOT_200,
)
def update_data(
    session: SessionDep,
    category: CategoryDTO,
    category_id: int = Path(alias="categoryId"),
    user: User = Depends(JWTBearer()),
):
    CategoryService(session, user).update_record(category, category_id)
    response = get_empty_response()
    return response


@router.delete(
    path="/{categoryId}",
    response_model=None,
    responses=NOT_422 | NOT_200,
)
def delete_data(
    session: SessionDep,
    category_id: int = Path(alias="categoryId"),
    user: User = Depends(JWTBearer()),
):
    CategoryService(session, user).delete_record(category_id)
    response = get_empty_response()
    return response
