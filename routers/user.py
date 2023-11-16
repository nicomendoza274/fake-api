from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session, get_db
from schemas.user import UserCreate, UserLogin
from services.user_service import UserService

user_router = APIRouter()


@user_router.get("/api/user", tags=["User"], status_code=200)
def get_users(
    db: Session = Depends(get_db),
):
    result = UserService(db).get_users()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@user_router.post("/api/user", tags=["User"], status_code=200)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    result = UserService(db).create_user(user)
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@user_router.post("/api/auth", tags=["Auth"], status_code=200)
def login(user: UserLogin, db: Session = Depends(get_db)):
    result = UserService(db).login_user(user)
    if not result:
        return JSONResponse(
            status_code=401, content={"message": "incorrect username or password"}
        )

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(result),
    )
