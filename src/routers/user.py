from fastapi import APIRouter, Depends, Form, Path, Request, status

from core.database.database import SessionDep
from core.models.response import MultipleResponseData, ResponseData
from core.services.file import FileService
from core.utils.json_validate import validate_json_data
from core.utils.query import str_to_query
from core.utils.response import get_empty_response, get_multiple_response, get_response
from middlewares.jwt_bearer import JWTBearer
from models.user import CreateUserDTO, User, UserDTO, UserResponseDTO
from services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=MultipleResponseData[UserResponseDTO],
)
def list_data(
    session: SessionDep,
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
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
    "/{userId}",
    response_model=ResponseData[UserResponseDTO],
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
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
def create_data(
    session: SessionDep,
    request: Request,
    body: CreateUserDTO = Form(..., media_type="multipart/form-data"),
    current_user: User = Depends(JWTBearer()),
):
    """
        * **data**: This is a stringify object of user, for example:

        ```json
        {
            "firstName": "string",
            "lastName": "string",
            "email": "string",
            "password": "string",
            "pictureId": 0
        }
        ```

    * **picture**: This is an image file
    """
    user = validate_json_data(UserDTO, body.data)
    file_service = FileService(session, current_user)
    new_file = file_service.save_file(body.picture, request)
    user.picture_id = new_file.file_id if new_file else None
    UserService(session, current_user).create_record(user)
    response = get_empty_response(status.HTTP_201_CREATED)
    return response


@router.put(
    "/{userId}",
    response_model=None,
)
def update_data(
    session: SessionDep,
    request: Request,
    body: CreateUserDTO = Form(..., media_type="multipart/form-data"),
    user_id: int = Path(alias="userId"),
    current_user: User = Depends(JWTBearer()),
):
    """
    Parameters
    ----------
    * **data**: This is a stringify object of user, for example:

        ```json
        {
            "firstName": "string",
            "lastName": "string",
            "email": "string",
            "password": "string",
            "pictureId": 0
        }
        ```

    * **picture**: This is an image file
    """

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
    "/{userId}",
    response_model=None,
)
def delete_data(
    session: SessionDep,
    user_id: int = Path(alias="userId"),
    current_user: User = Depends(JWTBearer()),
):
    UserService(session, current_user).delete_record(user_id)
    response = get_empty_response()
    return response
