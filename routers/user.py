from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session, get_db
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

    if not result:
        content = {
            "Errors": [
                {
                    "Code": "GEN-4000",
                    "Exception": "NotFoundException",
                    "Message": "The requested resource does not exist.",
                }
            ]
        }
        return JSONResponse(status_code=401, content=content)

    return JSONResponse(status_code=200, content=result)


@user_router.put("/api/users/validate-code", tags=["Users"])
def validate_code(user: UserValidateCode, db: Session = Depends(get_db)):
    result = UserService(db).validate_code(user)

    if not result:
        content = {
            "Errors": [
                {
                    "Code": "GEN-1000",
                    "Exception": "UnauthorizedAccessException",
                    "Message": "One or more attributes of the request do not match the expected values.",
                }
            ]
        }

        return JSONResponse(status_code=400, content=content)

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(result),
    )


@user_router.put("/api/users/forgot-change-password", tags=["Users"])
def validate_code(user: UserForgotChangePassword, db: Session = Depends(get_db)):
    result = UserService(db).forgot_change_password(user)

    if not result:
        content = {
            "Errors": [
                {
                    "Code": "GEN-4000",
                    "Exception": "NotFoundException",
                    "Message": "The requested resource does not exist.",
                }
            ]
        }

        return JSONResponse(status_code=400, content=content)

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(result),
    )


@user_router.post("/api/auth", tags=["Auth"], status_code=200)
def login(user: UserLogin, db: Session = Depends(get_db)):
    result = UserService(db).login_user(user)
    if not result:
        content = {
            "Errors": [
                {
                    "Code": "GEN-2002",
                    "Exception": "InvalidCredentialException",
                    "Message": "The provided credentials (username or password) are incorrect.",
                }
            ]
        }

        return JSONResponse(status_code=401, content=content)

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(result),
    )
