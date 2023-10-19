from fastapi import APIRouter
from fastapi.responses import JSONResponse
from schemas.user import User, UserCreateModel
from config.database import Session
from models.user import User as UserModel
from utils.jwt_manager import create_token
from services.encrypt import encrypt_string

user_router = APIRouter()


@user_router.post("/api/users", tags=["Auth"], response_model=UserCreateModel,  status_code=200)
def create_user(user: User):
    db = Session()
    new_user = UserModel(email = user.email, hash=encrypt_string(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.post('/api/auth', tags=['Auth'], status_code=200)
def login(user: User):
    db = Session()
    hash = encrypt_string(user.password)
    result: UserModel = db.query(UserModel).filter(UserModel.email == user.email, UserModel.hash == hash).first()
    if not result:
        return JSONResponse(status_code=401, content={"message": "usuario o contraseña incorrectos"})
    token: str = create_token({"user_id": result.user_id, "email": result.email, "hash": result.hash})
    
    return JSONResponse(
        status_code=200, 
        content={
            "user_id": result.user_id,
            "email": result.email,
            "token": token
        }
    )