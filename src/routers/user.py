from fastapi import APIRouter, Depends, Form, Path, Query, Request, status

from core.constants.responses import NOT_200, NOT_201, NOT_422
from core.database.database import SessionDep
from core.models.response import MultipleResponseData, ResponseData
from core.services.file import FileService
from core.utils.json_validate import validate_json_data
from core.utils.query import str_to_query
from core.utils.response import get_empty_response, get_multiple_response, get_response
from docs.user import USER_DOC
from middlewares.jwt_bearer import JWTBearer
from models.user import CreateUserDTO, User, UserDTO, UserResponseDTO
from services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    path="",
    response_model=MultipleResponseData[UserResponseDTO],
    responses=NOT_422,
    summary="List users",
)
def list_data(
    session: SessionDep,
    start: int | None = Query(default=0, description="Starting index for pagination"),
    length: int | None = Query(default=15, description="Number of items per page"),
    query: str | None = Query(default=None, description="Base64 encoded string"),
    current_user: User = Depends(JWTBearer()),
):
    query_criteria = str_to_query(query)
    user_list, total_count = UserService(session, current_user).get_records(
        start, length, query_criteria
    )

    response = get_multiple_response(
        count=total_count,
        start=start,
        length=len(user_list) if length == 0 else length,
        data=user_list,
    )
    return response


@router.get(
    path="/{userId}",
    response_model=ResponseData[UserResponseDTO],
    responses=NOT_422,
    summary="Get user",
)
def get_data(
    session: SessionDep,
    user_id: int = Path(alias="userId"),
    current_user: User = Depends(JWTBearer()),
):
    user_data = UserService(session, current_user).get_record(user_id)
    response = get_response(user_data)
    return response


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    responses=NOT_422 | NOT_201,
    description=USER_DOC,
    summary="Create user",
)
def create_data(
    session: SessionDep,
    request: Request,
    body: CreateUserDTO = Form(..., media_type="multipart/form-data"),
    current_user: User = Depends(JWTBearer()),
):
    user = validate_json_data(UserDTO, body.data)
    file_service = FileService(session, current_user)
    new_file = file_service.save_file(body.picture, request)
    user.picture_id = new_file.file_id if new_file else None
    UserService(session, current_user).create_record(user)
    response = get_empty_response(status.HTTP_201_CREATED)
    return response


@router.put(
    path="/{userId}",
    response_model=None,
    responses=NOT_422 | NOT_200,
    description=USER_DOC,
    summary="Update user",
)
def update_data(
    session: SessionDep,
    request: Request,
    body: CreateUserDTO = Form(..., media_type="multipart/form-data"),
    user_id: int = Path(alias="userId"),
    current_user: User = Depends(JWTBearer()),
):
    user = validate_json_data(UserDTO, body.data)

    if not user.picture_id:
        file_service = FileService(session, current_user)
        file_service.delete_file(User, current_user.user_id, "picture_id")
        new_file = file_service.save_file(body.picture, request)
        user.picture_id = new_file.file_id if new_file else None

    UserService(session, current_user).update_record(user, user_id)
    response = get_empty_response()
    return response


@router.delete(
    path="/{userId}",
    response_model=None,
    responses=NOT_422 | NOT_200,
    summary="Delete user",
)
def delete_data(
    session: SessionDep,
    user_id: int = Path(alias="userId"),
    current_user: User = Depends(JWTBearer()),
):
    UserService(session, current_user).delete_record(user_id)
    response = get_empty_response()
    return response
