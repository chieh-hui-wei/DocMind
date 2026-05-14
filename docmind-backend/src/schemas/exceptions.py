"""
src/schemas/exceptions.py
Custom exception classes used across the application.
"""
from src.errorcodes.errors import ErrorCode, ERROR_MESSAGES


class DocMindException(Exception):
    """Base exception for DocMind."""

    def __init__(
        self,
        error_code: ErrorCode,
        detail: str | None = None,
        status_code: int = 500,
    ):
        self.error_code = error_code
        self.detail = detail or ERROR_MESSAGES.get(error_code, "Unknown error")
        self.status_code = status_code
        super().__init__(self.detail)


class DocumentException(DocMindException):
    """Raised for document-related errors."""


class ChatException(DocMindException):
    """Raised for chat/LLM-related errors."""


class VectorDBException(DocMindException):
    """Raised for vector database errors."""


class NotFoundException(DocMindException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            error_code=ErrorCode.NOT_FOUND,
            detail=f"{resource} not found.",
            status_code=404,
        )
