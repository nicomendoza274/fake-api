import logging

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from src.core.classes.handle_exception import HandleException
from src.core.utils.response import get_error_response


class ErrorHandler(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

    def setup_logging(self) -> None:
        logging.basicConfig(
            filename="error.log",
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except HandleException as e:
            errors = e.errors
            status_error = e.status_code
            return get_error_response(errors=errors, status_code=status_error)

        except Exception as e:
            self.logger.exception("Error in request")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e)
            )
