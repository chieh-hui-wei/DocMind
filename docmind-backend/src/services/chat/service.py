"""
src/services/chat/service.py
Chat (RAG) service — retrieval-augmented generation pipeline.
Retrieves relevant context → constructs prompt → calls LLM → returns answer.
"""
from loguru import logger

from src.configs.settings import settings
from src.dbs.vector.vector_repository import vector_repository
from src.errorcodes.errors import ErrorCode
from src.schemas.exceptions import ChatException
from src.utils.embedding_client import embedding_client
from src.utils.llm_client import llm_client

SYSTEM_PROMPT = """You are DocMind, an intelligent AI assistant specialized in answering questions based on provided document context.

Your behavior rules:
1. Answer ONLY based on the provided context. Do not use external knowledge.
2. If the context doesn't contain enough information to answer, say so clearly.
3. Cite relevant passages when possible (e.g., "According to the document...").
4. Be concise and precise. Avoid unnecessary padding.
5. Format your answers in clear, readable markdown when appropriate.

You will be given:
- CONTEXT: relevant excerpts retrieved from the user's documents
- QUESTION: the user's question

Answer the QUESTION using only the CONTEXT."""


class ChatService:

    async def answer(
        self,
        question: str,
        doc_id: str | None = None,
    ) -> dict:
        """
        Full RAG pipeline:
        1. Embed the question
        2. Retrieve top-k similar chunks from vector store
        3. Build context string
        4. Call LLM with system prompt + context + question
        5. Return answer + source chunks
        """
        logger.info(f"RAG query: '{question[:80]}...' doc_id={doc_id}")

        # 1. Embed question
        query_embedding = embedding_client.embed_query(question)

        # 2. Retrieve context
        chunks = await vector_repository.similarity_search(
            query_embedding=query_embedding,
            top_k=settings.TOP_K_RESULTS,
            doc_id=doc_id,
        )

        if not chunks:
            raise ChatException(
                error_code=ErrorCode.NO_RELEVANT_CONTEXT,
                detail="No relevant documents found. Please upload documents first.",
                status_code=404,
            )

        # Filter by similarity threshold
        relevant = [c for c in chunks if c["score"] >= settings.SIMILARITY_THRESHOLD]
        if not relevant:
            raise ChatException(
                error_code=ErrorCode.NO_RELEVANT_CONTEXT,
                detail="Your documents don't contain information relevant to this question.",
                status_code=404,
            )

        # 3. Build context
        context_parts = []
        for i, chunk in enumerate(relevant, 1):
            fname = chunk["metadata"].get("filename", "unknown")
            context_parts.append(f"[Source {i} — {fname}]\n{chunk['content']}")
        context_str = "\n\n---\n\n".join(context_parts)

        # 4. Call LLM
        user_message = f"CONTEXT:\n{context_str}\n\nQUESTION:\n{question}"
        answer_text = await llm_client.chat(
            system_prompt=SYSTEM_PROMPT,
            user_message=user_message,
        )

        logger.info(f"Answer generated ({len(answer_text)} chars)")

        return {
            "answer": answer_text,
            "sources": [
                {
                    "filename": c["metadata"].get("filename"),
                    "chunk_index": c["metadata"].get("chunk_index"),
                    "score": round(c["score"], 4),
                    "excerpt": c["content"][:200] + "..." if len(c["content"]) > 200 else c["content"],
                }
                for c in relevant
            ],
        }


chat_service = ChatService()
