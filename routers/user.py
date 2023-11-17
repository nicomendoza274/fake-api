from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session, get_db
from constants.error import GEN_2002
from schemas.error import Errors
from schemas.user import (
    UserCreate,
    UserForgotChangePassword,
    UserLogin,
    UserSendCode,
    UserValidateCode,
)
from services.user_service import UserService

user_router = APIRouter()


@user_router.get("/api/users", tags=["Users"], status_code=200)
def get_users(
    db: Session = Depends(get_db),
):
    result = UserService(db).get_users()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@user_router.post("/api/users", tags=["Users"], status_code=200)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    result = UserService(db).create_user(user)
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@user_router.post("/api/users/send-code", tags=["Users"])
async def send_code(user: UserSendCode, db: Session = Depends(get_db)):
    result = await UserService(db).send_code(user)
    return result


@user_router.put("/api/users/validate-code", tags=["Users"])
def validate_code(user: UserValidateCode, db: Session = Depends(get_db)):
    result = UserService(db).validate_code(user)
    return result


@user_router.put("/api/users/forgot-change-password", tags=["Users"])
def change_password(user: UserForgotChangePassword, db: Session = Depends(get_db)):
    result = UserService(db).forgot_change_password(user)
    return result


@user_router.post("/api/auth", tags=["Auth"], status_code=200)
def login(user: UserLogin, db: Session = Depends(get_db)):
    result = UserService(db).login_user(user)
    if not result:
        content = Errors(Errors=[GEN_2002]).model_dump()
        return JSONResponse(status_code=401, content=content)

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(result),
    )
