"""
DocMind - AI-Powered Document Q&A System
Entry point: FastAPI application initialization and router registration.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.configs.settings import settings
from src.handlers.exception_handler import register_exception_handlers
from src.middleware.logging_middleware import LoggingMiddleware
from src.controllers.documents.web_apis import router as documents_router
from src.controllers.chat.web_apis import router as chat_router
from src.controllers.health.web_apis import router as health_router
from src.dbs.vector.chroma_client import chroma_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info(f"Starting DocMind API — env: {settings.ENV}")
    await chroma_client.initialize()
    yield
    logger.info("Shutting down DocMind API")
    await chroma_client.close()


app = FastAPI(
    title="DocMind API",
    description="RAG-powered document Q&A system with LLM integration",
    version="1.0.0",
    lifespan=lifespan,
)

# ── Middleware ─────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

# ── Exception Handlers ─────────────────────────────────────────────────────────
register_exception_handlers(app)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(health_router, prefix="/api/v1", tags=["Health"])
app.include_router(documents_router, prefix="/api/v1", tags=["Documents"])
app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])
