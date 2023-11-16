from typing import List

from fastapi import APIRouter, Depends, Query, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
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
    if not user:
        return Response(status_code=401)

    response = ProductService(db).get_records(start, length, query)

    return JSONResponse(status_code=200, content=response)


@product_router.get(
    "/api/product/{id}",
    tags=["Product"],
    status_code=200,
    response_model=Product | dict,
)
def get_product(
    id: int, db: Session = Depends(get_db), user: UserModel = Depends(JWTBearer())
):
    if not user:
        return Response(status_code=401)

    result = ProductService(db).get_record(id)

    return ProductService(db).response(result)


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
    if not user:
        return Response(status_code=401)

    product.product_id = None
    user_id = user.user_id
    result = ProductService(db).create_record(product, user_id)

    return JSONResponse(status_code=201, content=jsonable_encoder(result))


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
    if not user:
        return Response(status_code=401)

    user_id = user.user_id
    result = ProductService(db).update_record(product, user_id, product.product_id)

    return ProductService(db).response(result)


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
    if not user:
        return Response(status_code=401)

    user_id = user.user_id
    result = ProductService(db).tooggle_active(data, user_id, id)

    return ProductService(db).response(result)


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
    if not user:
        return Response(status_code=401)

    user_id = user.user_id
    result = ProductService(db).delete_multiple(ids, user_id)

    return ProductService(db).response(result)


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
    if not user:
        return Response(status_code=401)

    user_id = user.user_id
    result = ProductService(db).delete_record(id, user_id)

    return ProductService(db).response(result)
