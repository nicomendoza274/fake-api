import logging

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from core.classes.generic_errors import GenericError
from core.schemas.error import Errors


class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename="error.log",
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except GenericError as e:
            error = e.error
            status_error = (
                error.Status if error.Status else status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            content = Errors(Errors=[error]).model_dump()
            return JSONResponse(status_code=status_error, content=content)
        except Exception as e:
            self.logger.exception("Error in request")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e)
            )
