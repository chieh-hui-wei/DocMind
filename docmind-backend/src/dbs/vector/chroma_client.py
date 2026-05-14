"""
src/dbs/vector/chroma_client.py
ChromaDB vector database client — connection pool and base operations.
Encapsulates all vector DB interactions, isolated from business logic.
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from loguru import logger

from src.configs.settings import settings


class ChromaClient:
    """Singleton wrapper around the ChromaDB persistent client."""

    def __init__(self):
        self._client: chromadb.PersistentClient | None = None
        self._collection = None

    async def initialize(self) -> None:
        logger.info(f"Initializing ChromaDB at {settings.CHROMA_PERSIST_DIR}")
        self._client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(
            f"ChromaDB ready — collection '{settings.CHROMA_COLLECTION_NAME}' "
            f"has {self._collection.count()} documents"
        )

    async def close(self) -> None:
        # ChromaDB persistent client doesn't require explicit teardown
        logger.info("ChromaDB client closed")

    @property
    def collection(self):
        if self._collection is None:
            raise RuntimeError("ChromaDB not initialized. Call initialize() first.")
        return self._collection


chroma_client = ChromaClient()
