"""
src/utils/embedding_client.py
Local sentence-transformers embedding model wrapper.
Generates dense vector embeddings for text chunks and queries.
"""
from functools import lru_cache
from typing import List

from loguru import logger
from sentence_transformers import SentenceTransformer

from src.configs.settings import settings
from src.errorcodes.errors import ErrorCode
from src.schemas.exceptions import VectorDBException


class EmbeddingClient:
    def __init__(self):
        self._model: SentenceTransformer | None = None

    def _load(self) -> SentenceTransformer:
        if self._model is None:
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            self._model = SentenceTransformer(settings.EMBEDDING_MODEL)
            logger.info("Embedding model loaded")
        return self._model

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        try:
            model = self._load()
            vectors = model.encode(texts, normalize_embeddings=True)
            return vectors.tolist()
        except Exception as e:
            logger.exception(f"Embedding failed: {e}")
            raise VectorDBException(
                error_code=ErrorCode.EMBEDDING_FAILED,
                detail=str(e),
                status_code=500,
            )

    def embed_query(self, query: str) -> List[float]:
        return self.embed_texts([query])[0]


embedding_client = EmbeddingClient()
