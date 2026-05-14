"""
src/services/documents/service.py
Document ingestion service — parsing, chunking, embedding, and storage.
Controllers call this; this layer calls repositories and utils.
"""
import io
import uuid
from datetime import datetime, timezone
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

from src.configs.settings import settings
from src.dbs.vector.vector_repository import vector_repository
from src.errorcodes.errors import ErrorCode
from src.schemas.exceptions import DocumentException
from src.utils.embedding_client import embedding_client


class DocumentService:

    def __init__(self):
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    async def ingest_document(
        self,
        filename: str,
        content: bytes,
        content_type: str,
    ) -> dict:
        """
        Full ingestion pipeline:
        1. Parse raw bytes → text
        2. Split text → chunks
        3. Embed chunks
        4. Store in vector DB
        Returns document metadata.
        """
        doc_id = str(uuid.uuid4())
        logger.info(f"Ingesting document: {filename} (doc_id={doc_id})")

        # 1. Parse
        text = self._parse(filename, content)
        if not text.strip():
            raise DocumentException(
                error_code=ErrorCode.DOCUMENT_PARSE_FAILED,
                detail="Document appears to be empty or unreadable.",
                status_code=422,
            )

        # 2. Chunk
        chunks = self._splitter.split_text(text)
        logger.info(f"Split into {len(chunks)} chunks")

        # 3. Embed
        embeddings = embedding_client.embed_texts(chunks)

        # 4. Store
        metadatas = [
            {
                "doc_id": doc_id,
                "filename": filename,
                "chunk_index": i,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            for i in range(len(chunks))
        ]
        await vector_repository.upsert_chunks(doc_id, chunks, embeddings, metadatas)

        return {
            "doc_id": doc_id,
            "filename": filename,
            "chunk_count": len(chunks),
            "created_at": metadatas[0]["created_at"],
        }

    async def list_documents(self) -> List[dict]:
        """Return all ingested document metadata."""
        raw = await vector_repository.list_documents()
        return [
            {
                "doc_id": m["doc_id"],
                "filename": m["filename"],
                "created_at": m.get("created_at"),
            }
            for m in raw
        ]

    async def delete_document(self, doc_id: str) -> None:
        """Remove a document and all its chunks from the vector store."""
        await vector_repository.delete_document(doc_id)
        logger.info(f"Document {doc_id} deleted")

    # ── Private helpers ────────────────────────────────────────────────────────

    def _parse(self, filename: str, content: bytes) -> str:
        ext = filename.rsplit(".", 1)[-1].lower()

        if ext == "txt" or ext == "md":
            return content.decode("utf-8", errors="ignore")

        if ext == "pdf":
            return self._parse_pdf(content)

        if ext == "docx":
            return self._parse_docx(content)

        raise DocumentException(
            error_code=ErrorCode.UNSUPPORTED_FILE_TYPE,
            detail=f"Unsupported file type: .{ext}",
            status_code=415,
        )

    def _parse_pdf(self, content: bytes) -> str:
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(content))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            raise DocumentException(
                error_code=ErrorCode.DOCUMENT_PARSE_FAILED,
                detail=f"PDF parse error: {e}",
                status_code=422,
            )

    def _parse_docx(self, content: bytes) -> str:
        try:
            from docx import Document
            doc = Document(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            raise DocumentException(
                error_code=ErrorCode.DOCUMENT_PARSE_FAILED,
                detail=f"DOCX parse error: {e}",
                status_code=422,
            )


document_service = DocumentService()
