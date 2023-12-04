from fastapi import Request
from fastapi.security import HTTPBearer

from config.database import Session
from services.user_service import UserService
from utils.encrypt import validate_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        try:
            db = Session()
            auth = await super().__call__(request)

            credentials = validate_token(auth.credentials)
            result = UserService(db).get_user_by_credentials(credentials)

            if not result:
                return None
            db.close()
            return result
        except:
            return None
