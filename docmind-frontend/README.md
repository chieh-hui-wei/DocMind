# DocMind Frontend

A React + TypeScript frontend for the DocMind RAG system.  
Communicates with the FastAPI backend via REST API.

## Tech Stack

- **React 18** + TypeScript
- **Vite** (dev server + build)
- **react-dropzone** — drag-and-drop file upload
- **react-markdown** + remark-gfm — renders LLM markdown output
- **react-hot-toast** — notifications
- **lucide-react** — icons
- **axios** — HTTP client

## Structure

```
src/
├── App.tsx              # Root component — full UI layout
├── hooks/
│   ├── useDocuments.ts  # Document CRUD state management
│   └── useChat.ts       # Chat message state management
├── utils/
│   └── api.ts           # Centralized API client (axios)
└── styles/
    ├── globals.css      # Design system tokens + base styles
    └── app.css          # Component styles
```

## Quick Start

```bash
npm install
npm run dev
# → http://localhost:5173
```

The Vite dev server proxies `/api/*` to `http://localhost:8000`, so no CORS issues during development.

## Features

- **Drag & drop upload** — PDF, DOCX, TXT, MD files
- **Document library** — list and delete ingested documents  
- **Scoped search** — click a document to search only within it
- **RAG chat** — answers with cited source excerpts and similarity scores
- **Markdown rendering** — LLM responses rendered with full markdown support
