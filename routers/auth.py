from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from config.database import get_db
from schemas.user import UserLogin
from services.user_service import UserService

auth_router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"],
)


@auth_router.post("")
def login(user: UserLogin, db: Session = Depends(get_db)):
    response = UserService(db).login_user(user)
    return response
