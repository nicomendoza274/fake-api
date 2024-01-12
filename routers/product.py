from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm.session import Session

from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from models.user import User as UserModel
from schemas.product import Product, ProductActiveToggle, ProductUpdate
from services.product_service import ProductService

product_router = APIRouter(
    prefix="/api/products",
    tags=["Products"],
)


@product_router.get("")
def list(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    response = ProductService(db, user).get_records(start, length, query)
    return response


@product_router.get("/{id}", response_model=Product | dict)
def get(id: int, db: Session = Depends(get_db), user: UserModel = Depends(JWTBearer())):
    response = ProductService(db, user).get_record(id)
    return response


@product_router.post("", status_code=201, response_model=Product | dict)
def create(
    product: Product,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    product.product_id = None
    user_id = user.user_id
    response = ProductService(db, user).create_record(product, user_id)
    return response


@product_router.put("", response_model=Product | dict)
def update(
    product: ProductUpdate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = ProductService(db, user).update_record(
        product, user_id, product.product_id
    )
    return response


@product_router.put("/activate/{id}", response_model=Product | dict)
def toggle_active(
    id: int,
    data: ProductActiveToggle,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = ProductService(db, user).tooggle_active(data, user_id, id)
    return response


@product_router.delete("/multiple", response_model=dict)
async def delete_multiple(
    ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = ProductService(db, user).delete_multiple(ids, user_id)
    return response


@product_router.delete("/{id}", response_model=dict)
def delete(
    id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = ProductService(db, user).delete_record(id, user_id)
    return response
