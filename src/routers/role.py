from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm.session import Session

from core.database.database import get_db
from core.schemas.response import MultipleResponseData, ResponseData
from core.utils.query import str_to_query
from core.utils.response import get_empty_response, get_multiple_response, get_response
from middlewares.jwt_bearer import JWTBearer
from models.models import User
from schemas.role import RoleDTO, RoleResponseDTO
from services.role import RoleService

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@router.get(
    "",
    response_model=MultipleResponseData[list[RoleResponseDTO]],
)
def list_data(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    query_criteria = str_to_query(query)
    role_list, total_count = RoleService(db, user).get_records(
        start, length, query_criteria
    )
    response = get_multiple_response(
        count=total_count,
        start=start,
        length=len(role_list) if length == 0 else length,
        data=role_list,
    )
    return response


@router.get(
    "/{roleId}",
    response_model=ResponseData[RoleResponseDTO],
)
def get(
    role_id: int = Path(alias="roleId"),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    role_data = RoleService(db, user).get_record(role_id)
    response = get_response(role_data)
    return response


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
def create(
    role: RoleDTO,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    RoleService(db, user).create_record(role)
    response = get_empty_response(status.HTTP_201_CREATED)
    return response


@router.put(
    "/{roleId}",
    response_model=None,
)
def update(
    role: RoleDTO,
    role_id: int = Path(alias="roleId"),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    RoleService(db, user).update_record(role, role_id)
    response = get_empty_response()
    return response


@router.delete(
    "/multiple",
    response_model=None,
)
async def delete_multiple(
    ids: list[int] = Query(...),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    RoleService(db, user).delete_multiple(ids)
    response = get_empty_response()
    return response


@router.delete(
    "/{roleId}",
    response_model=None,
)
def delete(
    role_id: int = Path(alias="roleId"),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    RoleService(db, user).delete_record(role_id)
    response = get_empty_response()
    return response
