from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm.session import Session

from core.database.database import get_db
from core.schemas.response import MultipleResponseData, ResponseData
from core.utils.query import str_to_query
from core.utils.response import get_empty_response, get_multiple_response, get_response
from middlewares.jwt_bearer import JWTBearer
from models.models import User
from schemas.category import CategoryDTO, CategoryResponseDTO
from services.category import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get(
    "",
    response_model=MultipleResponseData[list[CategoryResponseDTO]],
)
def list_data(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    query_criteria = str_to_query(query)

    category_list, total_count = CategoryService(db, user).get_records(
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
    "/{categoryId}",
    response_model=ResponseData[CategoryResponseDTO],
)
def get(
    category_id: int = Path(alias="categoryId"),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    category_data = CategoryService(db, user).get_record(category_id)
    response = get_response(category_data)
    return response


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
def create(
    category: CategoryDTO,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    CategoryService(db, user).create_record(category)
    response = get_empty_response(status.HTTP_201_CREATED)
    return response


@router.put(
    "/{categoryId}",
    response_model=None,
)
def update(
    category: CategoryDTO,
    category_id: int = Path(alias="categoryId"),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    CategoryService(db, user).update_record(category, category_id)
    response = get_empty_response()
    return response


@router.delete(
    "/multiple",
    response_model=None,
)
async def delete_multiple(
    ids: list[int] = Query(...),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    CategoryService(db, user).delete_multiple(ids)
    response = get_empty_response()
    return response


@router.delete(
    "/{categoryId}",
    response_model=None,
)
def delete(
    category_id: int = Path(alias="categoryId"),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    CategoryService(db, user).delete_record(category_id)
    response = get_empty_response()
    return response
