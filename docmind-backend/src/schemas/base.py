"""
src/schemas/base.py
Shared Pydantic response models used across domains.
"""
from typing import Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "OK"
    data: T | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    error_code: str
    message: str
    detail: str | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    total: int
    page: int
    page_size: int
    data: list[T]
