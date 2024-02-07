from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from config.database import get_db
from schemas.user import (
    UserCreate,
    UserForgotChangePassword,
    UserLogin,
    UserSendCode,
    UserValidateCode,
)
from services.user_service import UserService

user_router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


@user_router.get("")
def list(db: Session = Depends(get_db)):
    response = UserService(db).get_users()
    return response


@user_router.post("")
def create(user: UserCreate, db: Session = Depends(get_db)):
    response = UserService(db).create_user(user)
    return response


@user_router.post("/send-code")
async def send_code(user: UserSendCode, db: Session = Depends(get_db)):
    response = await UserService(db).send_code(user)
    return response


@user_router.put("/validate-code")
def validate_code(user: UserValidateCode, db: Session = Depends(get_db)):
    response = UserService(db).validate_code(user)
    return response


@user_router.put("/forgot-change-password")
def change_password(user: UserForgotChangePassword, db: Session = Depends(get_db)):
    response = UserService(db).forgot_change_password(user)
    return response
