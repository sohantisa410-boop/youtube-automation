import logging
import time
from collections import defaultdict, deque

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration_ms = int((time.time() - start) * 1000)
        logger.info(
            "%s %s -> %s (%sms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers.setdefault(
            "Strict-Transport-Security",
            "max-age=63072000; includeSubDomains; preload",
        )
        response.headers.setdefault("X-Frame-Options", settings.security_frame_options)
        response.headers.setdefault(
            "X-Content-Type-Options", settings.security_content_type_options
        )
        response.headers.setdefault(
            "Referrer-Policy", settings.security_referrer_policy
        )
        response.headers.setdefault(
            "Permissions-Policy", settings.security_permissions_policy
        )
        response.headers.setdefault("Content-Security-Policy", settings.security_csp)
        return response


class BasicRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.limit = settings.rate_limit_per_minute
        self.requests: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        if request.url.path in {"/health", "/docs", "/openapi.json"}:
            return await call_next(request)

        now = time.time()
        window_start = now - 60
        client_key = request.headers.get("X-Forwarded-For") or (
            request.client.host if request.client else "unknown"
        )
        queue = self.requests[client_key]

        while queue and queue[0] < window_start:
            queue.popleft()

        if not queue:
            self.requests.pop(client_key, None)

        if len(queue) >= self.limit:
            return JSONResponse(
                status_code=429, content={"detail": "Rate limit exceeded"}
            )

        queue.append(now)
        return await call_next(request)
