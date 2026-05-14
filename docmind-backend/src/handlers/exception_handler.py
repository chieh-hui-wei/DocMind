"""
src/handlers/exception_handler.py
Global exception handlers registered on the FastAPI app.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger

from src.schemas.exceptions import DocMindException
from src.errorcodes.errors import ErrorCode


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(DocMindException)
    async def docmind_exception_handler(
        request: Request, exc: DocMindException
    ) -> JSONResponse:
        logger.warning(f"[{exc.error_code}] {exc.detail} — {request.url}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error_code": exc.error_code,
                "message": exc.detail,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        logger.warning(f"Validation error: {exc.errors()} — {request.url}")
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error_code": ErrorCode.VALIDATION_ERROR,
                "message": "Request validation failed.",
                "detail": exc.errors(),
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception(f"Unhandled exception: {exc} — {request.url}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error_code": ErrorCode.INTERNAL_SERVER_ERROR,
                "message": "An unexpected error occurred.",
            },
        )
