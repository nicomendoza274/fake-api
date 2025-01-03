from fastapi import APIRouter

from core.database.database import SessionDep
from core.models.response import ResponseData
from core.utils.response import get_empty_response, get_response
from models.auth import (
    UserCheckCodeDTO,
    UserForgotPasswordDTO,
    UserLoggedDTO,
    UserLoginDTO,
    UserResetPasswordDTO,
)
from services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/sign-in", response_model=ResponseData[UserLoggedDTO])
def login(session: SessionDep, user: UserLoginDTO):
    user_data = AuthService(session, None).login_user(user)
    response = get_response(user_data)
    return response


@router.post("/forgot-password", response_model=None)
async def forgot_password(session: SessionDep, user: UserForgotPasswordDTO):
    await AuthService(session, None).forgot_password(user)
    response = get_empty_response()
    return response


@router.post("/check-code", response_model=None)
def check_code(session: SessionDep, user: UserCheckCodeDTO):
    AuthService(session, None).check_code(user)
    response = get_empty_response()
    return response


@router.post("/reset-password", response_model=None)
def reset_password(session: SessionDep, user: UserResetPasswordDTO):
    AuthService(session, None).reset_password(user)
    response = get_empty_response()
    return response
