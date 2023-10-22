from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session
from models.user import User as UserModel
from schemas.user import User, UserCreateModel
from services.user_service import UserService
from utils.jwt_manager import create_token

user_router = APIRouter()


@user_router.post(
    "/api/users", tags=["Auth"], response_model=UserCreateModel, status_code=200
)
def create_user(user: User):
    db = Session()
    result = UserService(db).create_user(user)
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@user_router.post("/api/auth", tags=["Auth"], status_code=200)
def login(user: User):
    db = Session()
    result: UserModel = UserService(db).login_user(user)
    if not result:
        return JSONResponse(
            status_code=401, content={"message": "usuario o contraseña incorrectos"}
        )
    token: str = create_token(
        {"user_id": result.user_id, "email": result.email, "hash": result.hash}
    )

    return JSONResponse(
        status_code=200,
        content={"user_id": result.user_id, "email": result.email, "token": token},
    )
