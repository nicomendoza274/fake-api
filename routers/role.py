from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm.session import Session

from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from models.user import User as UserModel
from schemas.role import Role, RoleUpdate
from services.role_service import RoleService

role_router = APIRouter(
    prefix="/api/roles",
    tags=["Roles"],
)


@role_router.get("")
def list(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    response = RoleService(db, user).get_records(start, length, query)
    return response


@role_router.get("/{id}", response_model=Role | dict)
def get(id: int, db: Session = Depends(get_db), user: UserModel = Depends(JWTBearer())):
    response = RoleService(db, user).get_record(id)
    return response


@role_router.post("", status_code=201, response_model=Role | dict)
def create(
    role: Role,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    role.role_id = None
    user_id = user.user_id
    response = RoleService(db, user).create_record(role, user_id)
    return response


@role_router.put("", response_model=Role | dict)
def update(
    role: RoleUpdate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = RoleService(db, user).update_record(role, user_id, role.role_id)
    return response


@role_router.delete("/multiple", response_model=dict)
async def delete_multiple(
    ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = RoleService(db, user).delete_multiple(ids, user_id)
    return response


@role_router.delete("/{id}", response_model=dict)
def delete(
    id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = RoleService(db, user).delete_record(id, user_id)
    return response
