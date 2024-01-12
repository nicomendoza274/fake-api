from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm.session import Session

from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from models.user import User as UserModel
from schemas.user_role import UserRole, UserRoleUpdate
from services.user_role_service import UserRoleService

user_role_router = APIRouter(
    prefix="/api/userroles",
    tags=["UserRoles"],
)


@user_role_router.get("")
def list(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    response = UserRoleService(db, user).get_records(start, length, query)
    return response


@user_role_router.get("/{id}", response_model=UserRole | dict)
def get(
    id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    response = UserRoleService(db, user).get_record(id)
    return response


@user_role_router.post("", status_code=201, response_model=UserRole | dict)
def create(
    userRole: UserRole,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    userRole.user_role_id = None
    user_id = user.user_id
    response = UserRoleService(db, user).create_record(userRole, user_id)
    return response


@user_role_router.put("", response_model=UserRole | dict)
def update(
    userRole: UserRoleUpdate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = UserRoleService(db, user).update_record(
        userRole, user_id, userRole.user_role_id
    )
    return response


@user_role_router.delete("/multiple", response_model=dict)
async def delete_multiple(
    ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = UserRoleService(db, user).delete_multiple(ids, user_id)
    return response


@user_role_router.delete(
    "/{id}",
    response_model=dict,
)
def delete(
    id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = UserRoleService(db, user).delete_record(id, user_id)
    return response
