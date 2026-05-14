# DocMind Backend

A production-grade **RAG (Retrieval-Augmented Generation)** API built with **FastAPI** and **Gemini**.  
Follows a strict **Controller → Service → Repository** layered architecture.

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI + Uvicorn |
| LLM | Google Gemini (gemini-2.0-flash) |
| Embeddings | sentence-transformers (local, no API cost) |
| Vector Store | ChromaDB (persistent, local) |
| Document Parsing | pypdf, python-docx |
| Text Splitting | LangChain RecursiveCharacterTextSplitter |

## Architecture

```
src/
├── controllers/        # HTTP layer (routes, request/response models)
│   ├── documents/      # Upload, list, delete documents
│   └── chat/           # RAG Q&A endpoint
├── services/           # Business logic
│   ├── documents/      # Parsing → chunking → embedding → storage
│   └── chat/           # Retrieval → prompt construction → LLM call
├── dbs/
│   └── vector/         # ChromaDB client + CRUD repository
├── utils/
│   ├── llm_client.py   # Gemini API wrapper
│   └── embedding_client.py  # sentence-transformers wrapper
├── handlers/           # Global exception handlers
├── middleware/         # Logging, CORS
├── configs/            # Settings (pydantic-settings, .env)
├── errorcodes/         # Unified error codes
└── schemas/            # Shared Pydantic models + custom exceptions
```

## Quick Start

```bash
# 1. Clone and install
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Add your GOOGLE_API_KEY to .env
# Get one free at: https://aistudio.google.com/app/apikey

# 3. Run
uvicorn main:app --reload --port 8000
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/health/` | Health check |
| POST | `/api/v1/documents/upload` | Upload a document (PDF/TXT/DOCX/MD) |
| GET | `/api/v1/documents/` | List all documents |
| DELETE | `/api/v1/documents/{doc_id}` | Delete a document |
| POST | `/api/v1/chat/` | Ask a question (RAG) |

Interactive docs: **http://localhost:8000/docs**

## RAG Pipeline

```
User Question
    ↓
Embed question (sentence-transformers)
    ↓
Vector search in ChromaDB (cosine similarity)
    ↓
Retrieve top-k relevant chunks
    ↓
Build prompt: [System] + [Context chunks] + [Question]
    ↓
Call Gemini API
    ↓
Return answer + source citations
```

## Example Request

```bash
# Upload a document
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@your_document.pdf"

# Ask a question
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main findings?"}'
```
