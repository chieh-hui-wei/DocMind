"""
src/controllers/documents/models.py
Request and Response Pydantic models for the Documents domain.
"""
from datetime import datetime
from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    doc_id: str
    filename: str
    created_at: str | None = None


class UploadDocumentResponse(BaseModel):
    doc_id: str
    filename: str
    chunk_count: int
    created_at: str


class ListDocumentsResponse(BaseModel):
    documents: list[DocumentMetadata]
    total: int


class DeleteDocumentResponse(BaseModel):
    doc_id: str
    message: str = "Document deleted successfully"
