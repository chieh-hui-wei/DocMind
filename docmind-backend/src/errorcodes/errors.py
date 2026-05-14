"""
src/errorcodes/errors.py
Unified custom error codes and messages for the DocMind system.
"""
from enum import Enum


class ErrorCode(str, Enum):
    # General
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"

    # Document errors
    DOCUMENT_UPLOAD_FAILED = "DOCUMENT_UPLOAD_FAILED"
    DOCUMENT_NOT_FOUND = "DOCUMENT_NOT_FOUND"
    DOCUMENT_PARSE_FAILED = "DOCUMENT_PARSE_FAILED"
    UNSUPPORTED_FILE_TYPE = "UNSUPPORTED_FILE_TYPE"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"

    # Chat / RAG errors
    LLM_CALL_FAILED = "LLM_CALL_FAILED"
    NO_RELEVANT_CONTEXT = "NO_RELEVANT_CONTEXT"
    CHAT_SESSION_NOT_FOUND = "CHAT_SESSION_NOT_FOUND"

    # Vector DB errors
    VECTOR_DB_ERROR = "VECTOR_DB_ERROR"
    EMBEDDING_FAILED = "EMBEDDING_FAILED"


ERROR_MESSAGES: dict[ErrorCode, str] = {
    ErrorCode.INTERNAL_SERVER_ERROR: "An unexpected error occurred.",
    ErrorCode.VALIDATION_ERROR: "Request validation failed.",
    ErrorCode.NOT_FOUND: "Resource not found.",
    ErrorCode.DOCUMENT_UPLOAD_FAILED: "Failed to upload and process the document.",
    ErrorCode.DOCUMENT_NOT_FOUND: "The requested document does not exist.",
    ErrorCode.DOCUMENT_PARSE_FAILED: "Failed to extract text from the document.",
    ErrorCode.UNSUPPORTED_FILE_TYPE: "File type is not supported.",
    ErrorCode.FILE_TOO_LARGE: "File exceeds the maximum allowed size.",
    ErrorCode.LLM_CALL_FAILED: "LLM API call failed. Please try again.",
    ErrorCode.NO_RELEVANT_CONTEXT: "No relevant content found in your documents.",
    ErrorCode.CHAT_SESSION_NOT_FOUND: "Chat session not found.",
    ErrorCode.VECTOR_DB_ERROR: "Vector database operation failed.",
    ErrorCode.EMBEDDING_FAILED: "Failed to generate embeddings for the document.",
}
