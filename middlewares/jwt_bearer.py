from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from config.database import Session
from models.user import User as UserModel
from services.user_service import UserService
from utils.jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        db = Session()
        auth = await super().__call__(request)
        credentials = validate_token(auth.credentials)
        result: UserModel = UserService(db).get_user_by_credentials(credentials)

        if not result:
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")
        db.close()
        return result
