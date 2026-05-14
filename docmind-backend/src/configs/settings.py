"""
src/configs/settings.py
Global environment variable definitions and config loader.
Reads from .env or environment; supports local / dev / prd profiles.
"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ────────────────────────────────────────────────────────────────────
    ENV: str = "local"
    APP_NAME: str = "DocMind"
    DEBUG: bool = True
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # ── LLM ───────────────────────────────────────────────────────────────────
    GOOGLE_API_KEY: str = ""
    LLM_MODEL: str = "gemini-2.0-flash"
    LLM_MAX_TOKENS: int = 2048
    LLM_TEMPERATURE: float = 0.3

    # ── Embeddings ─────────────────────────────────────────────────────────────
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"   # local sentence-transformers model

    # ── Vector DB (ChromaDB) ───────────────────────────────────────────────────
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "docmind_docs"

    # ── Document Processing ────────────────────────────────────────────────────
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64
    MAX_FILE_SIZE_MB: int = 20
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "txt", "docx", "md"]

    # ── RAG ────────────────────────────────────────────────────────────────────
    TOP_K_RESULTS: int = 5
    SIMILARITY_THRESHOLD: float = 0.2


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
