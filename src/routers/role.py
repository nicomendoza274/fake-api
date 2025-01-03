from fastapi import APIRouter, Depends, Path, Query, status

from core.database.database import SessionDep
from core.models.response import MultipleResponseData, ResponseData
from core.utils.query import str_to_query
from core.utils.response import get_empty_response, get_multiple_response, get_response
from middlewares.jwt_bearer import JWTBearer
from models.role import RoleDTO, RoleResponseDTO
from models.user import User
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
    session: SessionDep,
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    user: User = Depends(JWTBearer()),
):
    query_criteria = str_to_query(query)
    role_list, total_count = RoleService(session, user).get_records(
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
    session: SessionDep,
    role_id: int = Path(alias="roleId"),
    user: User = Depends(JWTBearer()),
):
    role_data = RoleService(session, user).get_record(role_id)
    response = get_response(role_data)
    return response


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
def create(
    session: SessionDep,
    role: RoleDTO,
    user: User = Depends(JWTBearer()),
):
    RoleService(session, user).create_record(role)
    response = get_empty_response(status.HTTP_201_CREATED)
    return response


@router.put(
    "/{roleId}",
    response_model=None,
)
def update(
    session: SessionDep,
    role: RoleDTO,
    role_id: int = Path(alias="roleId"),
    user: User = Depends(JWTBearer()),
):
    RoleService(session, user).update_record(role, role_id)
    response = get_empty_response()
    return response


@router.delete(
    "/{roleId}",
    response_model=None,
)
def delete(
    session: SessionDep,
    role_id: int = Path(alias="roleId"),
    user: User = Depends(JWTBearer()),
):
    RoleService(session, user).delete_record(role_id)
    response = get_empty_response()
    return response
