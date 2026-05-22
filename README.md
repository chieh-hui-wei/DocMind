# DocMind — AI-Powered Document Q&A

> Upload documents. Ask questions. Get cited answers powered by RAG + Gemini.

A full-stack AI application demonstrating production patterns for LLM integration, RAG systems, and clean layered architecture.

## Architecture Overview

```
docmind/
├── docmind-backend/    # FastAPI + Python — RAG pipeline API
└── docmind-frontend/   # React + TypeScript — Document chat UI
```

### Backend: Controller → Service → Repository

```
Controllers  (HTTP routing, request validation)
    ↓
Services     (business logic: parse, chunk, embed, retrieve, generate)
    ↓
Repositories (vector DB CRUD — ChromaDB)
    ↓
Utils        (LLM client, embedding client)
```

### RAG Pipeline

```
[Document Upload]
  File → Parse → Chunk → Embed (local model) → Store in ChromaDB

[Question Answering]
  Question → Embed → Vector Search → Top-k Chunks → LLM Prompt → Answer + Citations
```

## Tech Stack

| | Backend | Frontend |
|---|---|---|
| **Framework** | FastAPI | React 18 + TypeScript |
| **LLM** | Google Gemini | — |
| **Embeddings** | sentence-transformers | — |
| **Vector DB** | ChromaDB (local) | — |
| **Doc Parsing** | pypdf, python-docx | — |
| **HTTP** | httpx, axios | axios |
| **Build** | uvicorn/gunicorn | Vite |

## Quick Start (Docker - Recommended)

```bash
# 1. Configure backend
cd docmind-backend
cp .env.example .env
# Add your GOOGLE_API_KEY to .env

# 2. Run everything from root
cd ..
docker-compose up -d --build
# Frontend → http://localhost:5174
# Backend Docs → http://localhost:8000/docs
```

## Manual Setup

### 1. Backend

```bash
cd docmind-backend
pip install -r requirements.txt
cp .env.example .env
# Add your GOOGLE_API_KEY to .env
uvicorn main:app --reload --port 8000
# Docs → http://localhost:8000/docs
```

### 2. Frontend

```bash
cd docmind-frontend
npm install
npm run dev
# → http://localhost:5173
```

## Key Engineering Decisions

**Why ChromaDB?** 

Zero-infrastructure local vector store — ideal for portfolio demos and prototypes. Swap to Pinecone/Weaviate/pgvector with one repository change.

**Why local embeddings?** 

`all-MiniLM-L6-v2` runs on CPU, incurs no API cost, and is fast enough for demo scale. Swap to OpenAI/Cohere embeddings by changing one config value.

**Why layered architecture?** 

Follows the project's existing Controller→Service→Repository pattern — keeps business logic testable, reusable, and decoupled from infrastructure.

**Why FastAPI?** 

Async-native, auto-generated OpenAPI docs, Pydantic validation — ideal for LLM APIs with potentially long response times.
