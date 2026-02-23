from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.classes.settings import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to basic rate limiting"""

    def __init__(self, app):
        super().__init__(app)
        self.requests: Dict[str, list] = defaultdict(list)
        self.rate_limit = settings.RATE_LIMIT_PER_MINUTE
        self.window_size = 60  # 60 secs

    def _get_client_ip(self, request: Request) -> str:
        """Get IP client"""

        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        return request.client.host if request.client else "unknown"

    def _cleanup_old_requests(self, client_ip: str) -> None:
        """Clear olds requests"""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.window_size)
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] if req_time > cutoff
        ]

    async def dispatch(self, request: Request, call_next):
        client_ip = self._get_client_ip(request)
        now = datetime.now()

        # Clear old requests
        self._cleanup_old_requests(client_ip)

        # Check rate limit
        if len(self.requests[client_ip]) >= self.rate_limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {self.rate_limit} requests per minute.",
            )

        # Register request
        self.requests[client_ip].append(now)

        response = await call_next(request)
        return response
