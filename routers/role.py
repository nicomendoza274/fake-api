from typing import List

from fastapi import APIRouter, Depends, Query, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session

from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from models.user import User as UserModel
from schemas.role import Role, RoleUpdate
from services.role_service import RoleService

role_router = APIRouter()


@role_router.get(
    "/api/role",
    tags=["Role"],
    status_code=200,
)
def get_roles(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    if not user:
        return Response(status_code=401)

    response = RoleService(db).get_records(start, length, query)

    return JSONResponse(status_code=200, content=response)


@role_router.get(
    "/api/role/{id}",
    tags=["Role"],
    status_code=200,
    response_model=Role | dict,
)
def get_role(
    id: int, db: Session = Depends(get_db), user: UserModel = Depends(JWTBearer())
):
    if not user:
        return Response(status_code=401)

    result = RoleService(db).get_record(id)

    return RoleService(db).response(result)


@role_router.post(
    "/api/role",
    tags=["Role"],
    status_code=201,
    response_model=Role | dict,
)
def create_role(
    role: Role,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    if not user:
        return Response(status_code=401)

    role.role_id = None
    user_id = user.user_id
    result = RoleService(db).create_record(role, user_id)

    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@role_router.put(
    "/api/role",
    tags=["Role"],
    status_code=200,
    response_model=Role | dict,
)
def update_role(
    role: RoleUpdate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    if not user:
        return Response(status_code=401)

    user_id = user.user_id
    result = RoleService(db).update_record(role, user_id, role.role_id)

    return RoleService(db).response(result)


@role_router.delete(
    "/api/role/multiple",
    tags=["Role"],
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
    result = RoleService(db).delete_multiple(ids, user_id)

    return RoleService(db).response(result)


@role_router.delete(
    "/api/role/{id}",
    tags=["Role"],
    response_model=dict,
    status_code=200,
)
def delete_role(
    id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    if not user:
        return Response(status_code=401)

    user_id = user.user_id
    result = RoleService(db).delete_record(id, user_id)

    return RoleService(db).response(result)
