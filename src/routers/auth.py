from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from core.database.database import get_db
from core.schemas.response import ResponseData
from core.utils.response import get_empty_response, get_response
from schemas.auth import (
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
def login(user: UserLoginDTO, db: Session = Depends(get_db)):
    user_data = AuthService(db, None).login_user(user)
    response = get_response(user_data)
    return response


@router.post(
    "/forgot-password",
    response_model=None,
)
async def forgot_password(
    user: UserForgotPasswordDTO,
    db: Session = Depends(get_db),
):
    await AuthService(db, None).forgot_password(user)
    response = get_empty_response()
    return response


@router.post(
    "/check-code",
    response_model=None,
)
def check_code(
    user: UserCheckCodeDTO,
    db: Session = Depends(get_db),
):
    AuthService(db, None).check_code(user)
    response = get_empty_response()
    return response


@router.post(
    "/reset-password",
    response_model=None,
)
def reset_password(
    user: UserResetPasswordDTO,
    db: Session = Depends(get_db),
):
    AuthService(db, None).reset_password(user)
    response = get_empty_response()
    return response
