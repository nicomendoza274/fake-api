from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm.session import Session

from core.database.database import get_db
from core.schemas.response import MultipleResponseData, ResponseData
from core.schemas.success_schema import SuccessDTO
from middlewares.jwt_bearer import JWTBearer
from models.models import User
from schemas.role import RoleDTO, RoleResponseDTO
from services.role import RoleService

role_router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@role_router.get("", response_model=MultipleResponseData[List[RoleResponseDTO]])
def list(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = RoleService(db, user).get_records(start, length, query)
    return response


@role_router.get("/{id}", response_model=ResponseData[RoleResponseDTO])
def get(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = RoleService(db, user).get_record(id)
    return response


@role_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData[RoleResponseDTO],
)
def create(
    role: RoleDTO,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = RoleService(db, user).create_record(role)
    return response


@role_router.put("", response_model=ResponseData[RoleResponseDTO])
def update(
    role: RoleDTO,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = RoleService(db, user).update_record(role, role.role_id)
    return response


@role_router.delete("/multiple", response_model=ResponseData[SuccessDTO])
async def delete_multiple(
    ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = RoleService(db, user).delete_multiple(ids)
    return response


@role_router.delete("/{id}", response_model=ResponseData[SuccessDTO])
def delete(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = RoleService(db, user).delete_record(id)
    return response
