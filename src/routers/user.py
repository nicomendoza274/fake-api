from fastapi import APIRouter, Depends, File, Form, Path, Request, UploadFile, status
from sqlalchemy.orm.session import Session

from core.database.database import get_db
from core.schemas.response import MultipleResponseData, ResponseData
from core.services.file import FileService
from core.utils.json_validate import validate_json_data
from core.utils.query import str_to_query
from core.utils.response import get_empty_response, get_multiple_response, get_response
from middlewares.jwt_bearer import JWTBearer
from models.models import User
from schemas.user import UserDTO, UserResponseDTO
from services.user import UserService

user = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user.get(
    "",
    response_model=MultipleResponseData[list[UserResponseDTO]],
)
def list(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(JWTBearer()),
):
    query_criteria = str_to_query(query)
    user_list, total_count = UserService(db, current_user).get_records(
        start, length, query_criteria
    )

    response = get_multiple_response(
        count=total_count,
        start=start,
        length=len(user_list) if length == 0 else length,
        data=user_list,
    )
    return response


@user.get(
    "/{userId}",
    response_model=ResponseData[UserResponseDTO],
)
def get(
    user_id: int = Path(alias="userId"),
    db: Session = Depends(get_db),
    current_user: User = Depends(JWTBearer()),
):
    user_data = UserService(db, current_user).get_record(user_id)
    response = get_response(user_data)
    return response


@user.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
def create(
    request: Request,
    json_data: str = Form(
        ...,
        alias="application/json",
        validation_alias="application/json",
    ),
    picture: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(JWTBearer()),
):
    """
        * **application/json**: This is a stringify object of user, for example:

        ```
        {
            "firstName": "string",
            "lastName": "string",
            "email": "string",
            "role_id": 0,
            "password": "string",
            "picture_id": 0
        }
        ```

    * **picture**: This is an image file
    """
    user = validate_json_data(UserDTO, json_data)
    file_service = FileService(db, current_user)
    new_file = file_service.save_file(picture, request)
    user.picture_id = new_file.file_id if new_file else None
    UserService(db, current_user).create_record(user)
    response = get_empty_response(status.HTTP_201_CREATED)
    return response


@user.put(
    "/{userId}",
    response_model=None,
)
def update(
    request: Request,
    user_id: int = Path(alias="userId"),
    json_data: str = Form(
        ...,
        alias="application/json",
        validation_alias="application/json",
    ),
    picture: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(JWTBearer()),
):
    """
    Parameters
    ----------
    * **application/json**: This is a stringify object of user, for example:

        ```
        {
            "firstName": "string",
            "lastName": "string",
            "email": "string",
            "role_id": 0,
            "password": "string",
            "pictureId": 0
        }
        ```

    * **picture**: This is an image file
    """

    user = validate_json_data(UserDTO, json_data)

    if not user.picture_id:
        file_service = FileService(db, current_user)
        file_service.delete_file(User, current_user.user_id, "picture_id")
        new_file = file_service.save_file(picture, request)
        user.picture_id = new_file.file_id if new_file else None

    UserService(db, current_user).update_record(user, user_id)
    response = get_empty_response()
    return response


@user.delete(
    "/{userId}",
    response_model=None,
)
def delete(
    user_id: int = Path(alias="userId"),
    db: Session = Depends(get_db),
    current_user: User = Depends(JWTBearer()),
):
    UserService(db, current_user).delete_record(user_id)
    response = get_empty_response()
    return response
