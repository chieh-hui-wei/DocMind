"""
src/controllers/documents/web_apis.py
Documents API router — file upload, listing, and deletion endpoints.
Delegates all logic to DocumentService.
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from loguru import logger

from src.configs.settings import settings
from src.controllers.documents.models import (
    UploadDocumentResponse,
    ListDocumentsResponse,
    DocumentMetadata,
    DeleteDocumentResponse,
)
from src.errorcodes.errors import ErrorCode
from src.schemas.base import BaseResponse
from src.schemas.exceptions import DocumentException
from src.services.documents.service import document_service

router = APIRouter(prefix="/documents")


@router.post("/upload", response_model=BaseResponse[UploadDocumentResponse])
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF, TXT, DOCX, MD) for ingestion into the knowledge base.
    The document is parsed, chunked, embedded, and stored in the vector database.
    """
    # Validate extension
    ext = (file.filename or "").rsplit(".", 1)[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise DocumentException(
            error_code=ErrorCode.UNSUPPORTED_FILE_TYPE,
            detail=f"Unsupported file type '.{ext}'. Allowed: {settings.ALLOWED_EXTENSIONS}",
            status_code=415,
        )

    # Validate file size
    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    if size_mb > settings.MAX_FILE_SIZE_MB:
        raise DocumentException(
            error_code=ErrorCode.FILE_TOO_LARGE,
            detail=f"File is {size_mb:.1f} MB; max allowed is {settings.MAX_FILE_SIZE_MB} MB.",
            status_code=413,
        )

    result = await document_service.ingest_document(
        filename=file.filename or "unnamed",
        content=content,
        content_type=file.content_type or "",
    )

    return BaseResponse(
        message="Document ingested successfully",
        data=UploadDocumentResponse(**result),
    )


@router.get("/", response_model=BaseResponse[ListDocumentsResponse])
async def list_documents():
    """List all documents currently stored in the knowledge base."""
    docs = await document_service.list_documents()
    return BaseResponse(
        data=ListDocumentsResponse(
            documents=[DocumentMetadata(**d) for d in docs],
            total=len(docs),
        )
    )


@router.delete("/{doc_id}", response_model=BaseResponse[DeleteDocumentResponse])
async def delete_document(doc_id: str):
    """Remove a document and all its chunks from the knowledge base."""
    await document_service.delete_document(doc_id)
    return BaseResponse(
        message="Document deleted",
        data=DeleteDocumentResponse(doc_id=doc_id),
    )
