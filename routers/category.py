from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm.session import Session

from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from models.user import User as UserModel
from schemas.category import Category, CategoryUpdate
from services.category_service import CategoryService

category_router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"],
)


@category_router.get("")
def list(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    response = CategoryService(db, user).get_records(start, length, query)
    return response


@category_router.get("/{id}", response_model=Category | dict)
def get(id: int, db: Session = Depends(get_db), user: UserModel = Depends(JWTBearer())):
    response = CategoryService(db, user).get_record(id)
    return response


@category_router.post("", status_code=201, response_model=Category | dict)
def create(
    category: Category,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    category.category_id = None
    user_id = user.user_id
    response = CategoryService(db, user).create_record(category, user_id)
    return response


@category_router.put("", response_model=Category | dict)
def update(
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = CategoryService(db, user).update_record(
        category, user_id, category.category_id
    )
    return response


@category_router.delete("/multiple", response_model=dict)
async def delete_multiple(
    ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = CategoryService(db, user).delete_multiple(ids, user_id)
    return response


@category_router.delete("/{id}", response_model=dict)
def delete(
    id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = CategoryService(db, user).delete_record(id, user_id)
    return response
