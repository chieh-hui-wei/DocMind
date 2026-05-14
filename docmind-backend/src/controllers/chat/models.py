"""
src/controllers/chat/models.py
Request and Response Pydantic models for the Chat domain.
"""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    doc_id: str | None = Field(
        default=None,
        description="Optionally scope the search to a specific document",
    )


class SourceChunk(BaseModel):
    filename: str | None
    chunk_index: int | None
    score: float
    excerpt: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
