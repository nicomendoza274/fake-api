from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from core.classes.generic_errors import GenericError
from core.constants.generic_errors import GEN_2000, GEN_2001, GEN_4000
from core.database.database import session
from core.utils.encrypt import validate_token
from services.user import UserService


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        try:
            db = session()
            auth = await super().__call__(request)

            if not auth:
                raise GenericError(GEN_2001)

            credentials = validate_token(auth.credentials)
            result = UserService(db, None).get_user_by_credentials(credentials)

            if not result:
                raise GenericError(GEN_4000)
            db.close()
            return result
        except HTTPException:
            raise GenericError(GEN_2001)
        except:
            raise GenericError(GEN_2000)
