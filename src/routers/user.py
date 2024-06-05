from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session

from core.database.database import get_db
from core.schemas.response import MultipleResponseData, ResponseData
from core.schemas.success_schema import SuccessDTO
from middlewares.jwt_bearer import JWTBearer
from models.models import User
from schemas.user import (
    UserDTO,
    UserForgotChangePasswordDTO,
    UserResponseDTO,
    UserSendCodeDTO,
    UserValidateCodeDTO,
)
from services.user import UserService

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user_router.get("", response_model=MultipleResponseData[List[UserResponseDTO]])
def list(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(JWTBearer()),
):
    response = UserService(db, current_user).get_records(start, length, query)
    return response


@user_router.get("/{id}", response_model=ResponseData[UserResponseDTO])
def get(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(JWTBearer()),
):
    response = UserService(db, current_user).get_record(id)
    return response


@user_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData[UserResponseDTO],
)
def create(
    user: UserDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(JWTBearer()),
):
    response = UserService(db, current_user).create_record(user)
    return response


@user_router.put("", response_model=ResponseData[UserResponseDTO])
def update(
    user: UserDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(JWTBearer()),
):
    response = UserService(db, current_user).update_record(user)
    return response


@user_router.delete("/{id}", response_model=ResponseData[SuccessDTO])
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(JWTBearer()),
):
    response = UserService(db, current_user).delete_record(id)
    return response


@user_router.post("/send-code", response_model=ResponseData[SuccessDTO])
async def send_code(
    user: UserSendCodeDTO,
    db: Session = Depends(get_db),
):
    response = await UserService(db, None).send_code(user)
    return response


@user_router.put("/validate-code", response_model=ResponseData[SuccessDTO])
def validate_code(
    user: UserValidateCodeDTO,
    db: Session = Depends(get_db),
):
    response = UserService(db, None).validate_code(user)
    return response


@user_router.put("/forgot-change-password", response_model=ResponseData[SuccessDTO])
def change_password(
    user: UserForgotChangePasswordDTO,
    db: Session = Depends(get_db),
):
    response = UserService(db, None).forgot_change_password(user)
    return response
