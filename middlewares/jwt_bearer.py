from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from config.database import Session
from models.user import User as UserModel
from utils.jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        db = Session()
        auth = await super().__call__(request)
        credentials = validate_token(auth.credentials)
        result: UserModel = (
            db.query(UserModel)
            .filter(
                UserModel.email == credentials["email"],
                UserModel.hash == credentials["hash"],
            )
            .first()
        )
        if not result:
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")
