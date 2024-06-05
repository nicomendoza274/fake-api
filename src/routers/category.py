from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm.session import Session

from core.database.database import get_db
from core.schemas.response import MultipleResponseData, ResponseData
from core.schemas.success_schema import SuccessDTO
from middlewares.jwt_bearer import JWTBearer
from models.models import User
from schemas.category import CategoryDTO, CategoryResponseDTO
from services.category import CategoryService

category_router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@category_router.get(
    "",
    response_model=MultipleResponseData[List[CategoryResponseDTO]],
)
def list(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = CategoryService(db, user).get_records(start, length, query)
    return response


@category_router.get(
    "/{id}",
    response_model=ResponseData[CategoryResponseDTO],
)
def get(id: int, db: Session = Depends(get_db), user: User = Depends(JWTBearer())):
    response = CategoryService(db, user).get_record(id)
    return response


@category_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData[CategoryResponseDTO],
)
def create(
    category: CategoryDTO,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = CategoryService(db, user).create_record(category)
    return response


@category_router.put(
    "",
    response_model=ResponseData[CategoryResponseDTO],
)
def update(
    category: CategoryDTO,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = CategoryService(db, user).update_record(category, category.category_id)
    return response


@category_router.delete(
    "/multiple",
    response_model=ResponseData[SuccessDTO],
)
async def delete_multiple(
    ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = CategoryService(db, user).delete_multiple(ids)
    return response


@category_router.delete(
    "/{id}",
    response_model=ResponseData[SuccessDTO],
)
def delete(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = CategoryService(db, user).delete_record(id)
    return response
