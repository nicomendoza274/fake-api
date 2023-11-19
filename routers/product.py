from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm.session import Session

from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from models.user import User as UserModel
from schemas.product import Product, ProductActiveToggle, ProductUpdate
from services.product_service import ProductService

product_router = APIRouter()


@product_router.get(
    "/api/product",
    tags=["Product"],
    status_code=200,
)
def get_products(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    response = ProductService(db, user).get_records(start, length, query)
    return response


@product_router.get(
    "/api/product/{id}",
    tags=["Product"],
    status_code=200,
    response_model=Product | dict,
)
def get_product(
    id: int, db: Session = Depends(get_db), user: UserModel = Depends(JWTBearer())
):
    response = ProductService(db, user).get_record(id)
    return response


@product_router.post(
    "/api/product",
    tags=["Product"],
    status_code=201,
    response_model=Product | dict,
)
def create_product(
    product: Product,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    product.product_id = None
    user_id = user.user_id
    response = ProductService(db, user).create_record(product, user_id)
    return response


@product_router.put(
    "/api/product",
    tags=["Product"],
    status_code=200,
    response_model=Product | dict,
)
def update_product(
    product: ProductUpdate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = ProductService(db, user).update_record(
        product, user_id, product.product_id
    )
    return response


@product_router.put(
    "/api/product/activate/{id}",
    tags=["Product"],
    status_code=200,
    response_model=Product | dict,
)
def toggle_active(
    id: int,
    data: ProductActiveToggle,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = ProductService(db, user).tooggle_active(data, user_id, id)
    return response


@product_router.delete(
    "/api/product/multiple",
    tags=["Product"],
    response_model=dict,
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
async def delete_multiple(
    ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = ProductService(db, user).delete_multiple(ids, user_id)
    return response


@product_router.delete(
    "/api/product/{id}",
    tags=["Product"],
    response_model=dict,
    status_code=200,
)
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = ProductService(db, user).delete_record(id, user_id)
    return response
