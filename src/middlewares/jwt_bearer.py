from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer

from core.classes.handle_exception import HandleException
from core.constants.generic_errors import GEN_2000, GEN_2001, GEN_4000
from core.database.database import SessionDep
from core.utils.encrypt import validate_token
from services.user import UserService


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request, session: SessionDep):
        try:
            auth = await super().__call__(request)

            if not auth:
                raise HandleException([GEN_2001], status.HTTP_401_UNAUTHORIZED)

            credentials = validate_token(auth.credentials)
            result = UserService(session, None).get_user_by_credentials(credentials)

            if not result:
                raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)
            return result
        except HTTPException:
            raise HandleException([GEN_2001], status.HTTP_401_UNAUTHORIZED)
        except:
            raise HandleException([GEN_2000], status.HTTP_401_UNAUTHORIZED)
