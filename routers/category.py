from typing import List

from fastapi import APIRouter, Depends, Query
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
    dependencies=[Depends(JWTBearer())],
)
def get_categories(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
):
    response = CategoryService(db=db).get_records(start, length, query)
    return JSONResponse(status_code=200, content=response)


@category_router.get(
    "/api/category/{id}",
    tags=["category"],
    status_code=200,
    response_model=Category | dict,
    dependencies=[Depends(JWTBearer())],
)
def get_category(id: int, db: Session = Depends(get_db)):
    result = CategoryService(db=db).get_record(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Not Found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@category_router.post(
    "/api/category",
    tags=["category"],
    status_code=201,
    response_model=Category | dict,
    dependencies=[Depends(JWTBearer())],
)
def create_category(
    category: Category,
    user: UserModel = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    category.category_id = None
    user_id = user.user_id
    result = CategoryService(db=db).create_record(category, user_id)
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@category_router.put(
    "/api/category",
    tags=["category"],
    status_code=200,
    response_model=Category | dict,
    dependencies=[Depends(JWTBearer())],
)
def update_category(
    category: CategoryUpdate,
    user: UserModel = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    user_id = user.user_id
    result = CategoryService(db=db).update_record(
        category, user_id, category.category_id
    )
    if not result:
        return JSONResponse(status_code=404, content={"message": "Not Found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@category_router.delete(
    "/api/category/multiple",
    tags=["prcategoryoduct"],
    response_model=dict,
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
async def delete_multiple(
    ids: List[int] = Query(...),
    user: UserModel = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    user_id = user.user_id
    result = CategoryService(db=db).delete_multiple(ids, user_id)

    if not result:
        return JSONResponse(status_code=404, content={"message": "Not Found"})

    return JSONResponse(content=result)


@category_router.delete(
    "/api/category/{id}",
    tags=["category"],
    response_model=dict,
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
def delete_category(
    id: int, user: UserModel = Depends(JWTBearer()), db: Session = Depends(get_db)
):
    user_id = user.user_id

    result = CategoryService(db=db).delete_record(id, user_id)

    if not result:
        return JSONResponse(status_code=404, content={"message": "Not Found"})

    return JSONResponse(content=result)
