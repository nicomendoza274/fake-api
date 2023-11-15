from typing import List

from fastapi import APIRouter, Depends, Query, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session

from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from models.user import User as UserModel
from schemas.category import Category, CategoryUpdate
from services.category_service import CategoryService

category_router = APIRouter()


@category_router.get(
    "/api/category",
    tags=["category"],
    status_code=200,
)
def get_categories(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    if not user:
        return Response(status_code=401)

    response = CategoryService(db).get_records(start, length, query)

    return JSONResponse(status_code=200, content=response)


@category_router.get(
    "/api/category/{id}",
    tags=["category"],
    status_code=200,
    response_model=Category | dict,
)
def get_category(
    id: int, db: Session = Depends(get_db), user: UserModel = Depends(JWTBearer())
):
    if not user:
        return Response(status_code=401)

    result = CategoryService(db).get_record(id)

    return CategoryService(db).response(result)


@category_router.post(
    "/api/category",
    tags=["category"],
    status_code=201,
    response_model=Category | dict,
)
def create_category(
    category: Category,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    if not user:
        return Response(status_code=401)

    category.category_id = None
    user_id = user.user_id
    result = CategoryService(db).create_record(category, user_id)

    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@category_router.put(
    "/api/category",
    tags=["category"],
    status_code=200,
    response_model=Category | dict,
)
def update_category(
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    if not user:
        return Response(status_code=401)

    user_id = user.user_id
    result = CategoryService(db).update_record(category, user_id, category.category_id)

    return CategoryService(db).response(result)


@category_router.delete(
    "/api/category/multiple",
    tags=["category"],
    response_model=dict,
    status_code=200,
)
async def delete_multiple(
    ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    if not user:
        return Response(status_code=401)

    user_id = user.user_id
    result = CategoryService(db).delete_multiple(ids, user_id)

    return CategoryService(db).response(result)


@category_router.delete(
    "/api/category/{id}",
    tags=["category"],
    response_model=dict,
    status_code=200,
)
def delete_category(
    id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    if not user:
        return Response(status_code=401)

    user_id = user.user_id
    result = CategoryService(db).delete_record(id, user_id)

    return CategoryService(db).response(result)
