"""
src/dbs/vector/vector_repository.py
CRUD operations for the vector store.
All vector DB interactions go through here — services never touch chromadb directly.
"""
import uuid
from typing import List

from loguru import logger

from src.dbs.vector.chroma_client import chroma_client
from src.errorcodes.errors import ErrorCode
from src.schemas.exceptions import VectorDBException


class VectorRepository:
    """Repository for document chunk storage and semantic search."""

    @property
    def _col(self):
        return chroma_client.collection

    async def upsert_chunks(
        self,
        doc_id: str,
        chunks: List[str],
        embeddings: List[List[float]],
        metadatas: List[dict],
    ) -> int:
        """Insert or update document chunks with their embeddings."""
        try:
            ids = [f"{doc_id}__chunk_{i}" for i in range(len(chunks))]
            self._col.upsert(
                ids=ids,
                documents=chunks,
                embeddings=embeddings,
                metadatas=metadatas,
            )
            logger.info(f"Upserted {len(chunks)} chunks for doc_id={doc_id}")
            return len(chunks)
        except Exception as e:
            logger.exception(f"ChromaDB upsert failed: {e}")
            raise VectorDBException(
                error_code=ErrorCode.VECTOR_DB_ERROR,
                detail=str(e),
                status_code=500,
            )

    async def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        doc_id: str | None = None,
    ) -> List[dict]:
        """Return top-k semantically similar chunks."""
        try:
            where = {"doc_id": doc_id} if doc_id else None
            results = self._col.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where,
                include=["documents", "metadatas", "distances"],
            )
            chunks = []
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
                chunks.append(
                    {"content": doc, "metadata": meta, "score": 1 - dist}
                )
            return chunks
        except Exception as e:
            logger.exception(f"ChromaDB query failed: {e}")
            raise VectorDBException(
                error_code=ErrorCode.VECTOR_DB_ERROR,
                detail=str(e),
                status_code=500,
            )

    async def delete_document(self, doc_id: str) -> None:
        """Delete all chunks for a given document."""
        try:
            results = self._col.get(where={"doc_id": doc_id}, include=[])
            if results["ids"]:
                self._col.delete(ids=results["ids"])
                logger.info(f"Deleted {len(results['ids'])} chunks for doc_id={doc_id}")
        except Exception as e:
            logger.exception(f"ChromaDB delete failed: {e}")
            raise VectorDBException(
                error_code=ErrorCode.VECTOR_DB_ERROR,
                detail=str(e),
                status_code=500,
            )

    async def list_documents(self) -> List[dict]:
        """Return unique document metadata records."""
        try:
            results = self._col.get(include=["metadatas"])
            seen: dict[str, dict] = {}
            for meta in results["metadatas"]:
                doc_id = meta.get("doc_id")
                if doc_id and doc_id not in seen:
                    seen[doc_id] = meta
            return list(seen.values())
        except Exception as e:
            logger.exception(f"ChromaDB list failed: {e}")
            raise VectorDBException(
                error_code=ErrorCode.VECTOR_DB_ERROR,
                detail=str(e),
                status_code=500,
            )


vector_repository = VectorRepository()
