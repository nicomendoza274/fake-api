from fastapi import APIRouter

from src.core.constants.responses import NOT_200, NOT_422
from src.core.database.database import SessionDep
from src.core.models.response import ResponseData
from src.core.utils.response import get_empty_response, get_response
from src.models.user import (
    UserCheckCodeDTO,
    UserForgotPasswordDTO,
    UserLoggedDTO,
    UserLoginDTO,
    UserResetPasswordDTO,
)
from src.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    path="/sign-in",
    response_model=ResponseData[UserLoggedDTO],
    responses=NOT_422,
    summary="Sign in user",
)
def login(session: SessionDep, user: UserLoginDTO):
    user_data = AuthService(session, None).login_user(user)
    response = get_response(user_data)
    return response


@router.post(
    path="/forgot-password",
    response_model=None,
    responses=NOT_422 | NOT_200,
    summary="Forgot user password",
)
async def forgot_password(session: SessionDep, user: UserForgotPasswordDTO):
    await AuthService(session, None).forgot_password(user)
    response = get_empty_response()
    return response


@router.post(
    path="/check-code",
    response_model=None,
    responses=NOT_422 | NOT_200,
    summary="Check code",
)
def check_code(session: SessionDep, user: UserCheckCodeDTO):
    AuthService(session, None).check_code(user)
    response = get_empty_response()
    return response


@router.post(
    path="/reset-password",
    response_model=None,
    responses=NOT_422 | NOT_200,
    summary="Reset user password",
)
def reset_password(session: SessionDep, user: UserResetPasswordDTO):
    AuthService(session, None).reset_password(user)
    response = get_empty_response()
    return response
