from fastapi import APIRouter, Depends, Path, Query, status

from core.constants.responses import NOT_200, NOT_201, NOT_422
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
    path="",
    response_model=MultipleResponseData[RoleResponseDTO],
    responses=NOT_422,
    summary="List roles",
)
def list_data(
    session: SessionDep,
    start: int | None = Query(default=0, description="Starting index for pagination"),
    length: int | None = Query(default=15, description="Number of items per page"),
    query: str | None = Query(default=None, description="Base64 encoded string"),
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
    path="/{roleId}",
    response_model=ResponseData[RoleResponseDTO],
    responses=NOT_422,
    summary="Get role",
)
def get_data(
    session: SessionDep,
    role_id: int = Path(alias="roleId"),
    user: User = Depends(JWTBearer()),
):
    role_data = RoleService(session, user).get_record(role_id)
    response = get_response(role_data)
    return response


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    responses=NOT_422 | NOT_201,
    summary="Create role",
)
def create_data(
    session: SessionDep,
    role: RoleDTO,
    user: User = Depends(JWTBearer()),
):
    RoleService(session, user).create_record(role)
    response = get_empty_response(status.HTTP_201_CREATED)
    return response


@router.put(
    path="/{roleId}",
    response_model=None,
    responses=NOT_422 | NOT_200,
    summary="Update role",
)
def update_data(
    session: SessionDep,
    role: RoleDTO,
    role_id: int = Path(alias="roleId"),
    user: User = Depends(JWTBearer()),
):
    RoleService(session, user).update_record(role, role_id)
    response = get_empty_response()
    return response


@router.delete(
    path="/{roleId}",
    response_model=None,
    responses=NOT_422 | NOT_200,
    summary="Delete role",
)
def delete_data(
    session: SessionDep,
    role_id: int = Path(alias="roleId"),
    user: User = Depends(JWTBearer()),
):
    RoleService(session, user).delete_record(role_id)
    response = get_empty_response()
    return response
