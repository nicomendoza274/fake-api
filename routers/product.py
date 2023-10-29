from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session, get_db
from middlewares.jwt_bearer import JWTBearer
from models.user import User as UserModel
from schemas.product import Product
from services.product_service import ProductService

product_router = APIRouter()


@product_router.get(
    "/api/product",
    tags=["product"],
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
def get_products(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
):
    response = ProductService(db).get_records(start, length, query)
    return JSONResponse(status_code=200, content=response)


@product_router.get(
    "/api/product/{id}",
    tags=["product"],
    status_code=200,
    response_model=Product | dict,
    dependencies=[Depends(JWTBearer())],
)
def get_product(id: int, db: Session = Depends(get_db)):
    result = ProductService(db).get_record(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Not Found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@product_router.post(
    "/api/product",
    tags=["product"],
    status_code=201,
    response_model=Product | dict,
    dependencies=[Depends(JWTBearer())],
)
def create_product(
    product: Product,
    user: UserModel = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    user_id = user.user_id
    result = ProductService(db).create_record(product, user_id)
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@product_router.put(
    "/api/product",
    tags=["product"],
    status_code=200,
    response_model=Product | dict,
    dependencies=[Depends(JWTBearer())],
)
def update_product(
    product: Product,
    user: UserModel = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    user_id = user.user_id
    result = ProductService(db).update_record(product, user_id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Not Found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@product_router.delete(
    "/api/product/{id}",
    tags=["product"],
    response_model=dict,
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
def delete_product(
    id: int, user: UserModel = Depends(JWTBearer()), db: Session = Depends(get_db)
):
    user_id = user.user_id

    result = ProductService(db).delete_record(id, user_id)

    if not result:
        return JSONResponse(status_code=404, content={"message": "Not Found"})

    return JSONResponse(content=result)
