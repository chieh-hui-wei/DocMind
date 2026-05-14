"""
src/middleware/logging_middleware.py
Global HTTP request/response logging middleware.
"""
import time
import uuid

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        start = time.perf_counter()

        logger.info(
            f"[{request_id}] → {request.method} {request.url.path}"
        )

        response = await call_next(request)

        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            f"[{request_id}] ← {response.status_code} ({elapsed_ms:.1f}ms)"
        )

        response.headers["X-Request-ID"] = request_id
        return response
