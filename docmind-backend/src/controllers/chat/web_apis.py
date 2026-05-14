"""
src/controllers/chat/web_apis.py
Chat API router — question answering via RAG pipeline.
"""
from fastapi import APIRouter

from src.controllers.chat.models import ChatRequest, ChatResponse
from src.schemas.base import BaseResponse
from src.services.chat.service import chat_service

router = APIRouter(prefix="/chat")


@router.post("/", response_model=BaseResponse[ChatResponse])
async def ask_question(payload: ChatRequest):
    """
    Ask a question against the ingested knowledge base.
    Uses RAG: retrieves relevant document chunks, then generates an LLM answer.
    Optionally scoped to a specific document via `doc_id`.
    """
    result = await chat_service.answer(
        question=payload.question,
        doc_id=payload.doc_id,
    )
    return BaseResponse(
        message="Answer generated",
        data=ChatResponse(**result),
    )
