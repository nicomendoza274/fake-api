from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from core.database.database import get_db
from core.schemas.response import ResponseData
from schemas.user import UserLoggedDTO, UserLoginDTO
from services.user import UserService

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.post("", response_model=ResponseData[UserLoggedDTO])
def login(user: UserLoginDTO, db: Session = Depends(get_db)):
    response = UserService(db, None).login_user(user)
    return response
