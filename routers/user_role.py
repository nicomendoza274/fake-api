from typing import List

from fastapi import APIRouter, Depends, Query, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session

from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from models.user import User as UserModel
from schemas.user_role import UserRole, UserRoleUpdate
from services.user_role_service import UserRoleService

user_role_router = APIRouter()


@user_role_router.get(
    "/api/userrole",
    tags=["UserRole"],
    status_code=200,
)
def get_user_roles(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    response = UserRoleService(db, user).get_records(start, length, query)
    return response


@user_role_router.get(
    "/api/userrole/{id}",
    tags=["UserRole"],
    status_code=200,
    response_model=UserRole | dict,
)
def get_user_role(
    id: int, db: Session = Depends(get_db), user: UserModel = Depends(JWTBearer())
):
    response = UserRoleService(db, user).get_record(id)
    return response


@user_role_router.post(
    "/api/userrole",
    tags=["UserRole"],
    status_code=201,
    response_model=UserRole | dict,
)
def create_user_role(
    userRole: UserRole,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    userRole.user_role_id = None
    user_id = user.user_id
    response = UserRoleService(db, user).create_record(userRole, user_id)
    return response


@user_role_router.put(
    "/api/userrole",
    tags=["UserRole"],
    status_code=200,
    response_model=UserRole | dict,
)
def update_user_role(
    userRole: UserRoleUpdate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = UserRoleService(db, user).update_record(
        userRole, user_id, userRole.user_role_id
    )
    return response


@user_role_router.delete(
    "/api/role/userrole",
    tags=["UserRole"],
    response_model=dict,
    status_code=200,
)
async def delete_multiple(
    ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = UserRoleService(db, user).delete_multiple(ids, user_id)
    return response


@user_role_router.delete(
    "/api/userrole/{id}",
    tags=["UserRole"],
    response_model=dict,
    status_code=200,
)
def delete_user_role(
    id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = UserRoleService(db, user).delete_record(id, user_id)
    return response
