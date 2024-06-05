from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm.session import Session

from core.database.database import get_db
from core.schemas.response import MultipleResponseData, ResponseData
from core.schemas.success_schema import SuccessDTO
from middlewares.jwt_bearer import JWTBearer
from models.models import User
from schemas.product import ProductActiveToggleDTO, ProductDTO, ProductResponseDTO
from services.product import ProductService

product_router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@product_router.get(
    "",
    response_model=MultipleResponseData[List[ProductResponseDTO]],
)
def list(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = ProductService(db, user).get_records(start, length, query)
    return response


@product_router.get(
    "/{id}",
    response_model=ResponseData[ProductResponseDTO],
)
def get(id: int, db: Session = Depends(get_db), user: User = Depends(JWTBearer())):
    response = ProductService(db, user).get_record(id)
    return response


@product_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData[ProductResponseDTO],
)
def create(
    product: ProductDTO,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = ProductService(db, user).create_record(product)
    return response


@product_router.put(
    "",
    response_model=ResponseData[ProductResponseDTO],
)
def update(
    product: ProductDTO,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = ProductService(db, user).update_record(product, product.product_id)
    return response


@product_router.put(
    "/activate/{id}",
    response_model=ResponseData[ProductResponseDTO],
)
def toggle_active(
    id: int,
    data: ProductActiveToggleDTO,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = ProductService(db, user).toggle_active(data, id)
    return response


@product_router.delete(
    "/multiple",
    response_model=ResponseData[SuccessDTO],
)
async def delete_multiple(
    ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = ProductService(db, user).delete_multiple(ids)
    return response


@product_router.delete(
    "/{id}",
    response_model=ResponseData[SuccessDTO],
)
def delete(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = ProductService(db, user).delete_record(id)
    return response
