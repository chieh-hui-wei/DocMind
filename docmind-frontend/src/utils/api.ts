// src/utils/api.ts
// Centralized API client — all backend communication goes through here.

import axios from 'axios'

const BASE = '/api/v1'

export const api = axios.create({
  baseURL: BASE,
  timeout: 60_000,
})

// ── Types ─────────────────────────────────────────────────────────────────────

export interface Document {
  doc_id: string
  filename: string
  created_at: string | null
}

export interface SourceChunk {
  filename: string | null
  chunk_index: number | null
  score: number
  excerpt: string
}

export interface ChatAnswer {
  answer: string
  sources: SourceChunk[]
}

// ── Documents ─────────────────────────────────────────────────────────────────

export async function uploadDocument(file: File): Promise<Document & { chunk_count: number }> {
  const form = new FormData()
  form.append('file', file)
  const res = await api.post('/documents/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data.data
}

export async function listDocuments(): Promise<Document[]> {
  const res = await api.get('/documents/')
  return res.data.data.documents
}

export async function deleteDocument(docId: string): Promise<void> {
  await api.delete(`/documents/${docId}`)
}

// ── Chat ──────────────────────────────────────────────────────────────────────

export async function askQuestion(question: string, docId?: string): Promise<ChatAnswer> {
  const res = await api.post('/chat/', { question, doc_id: docId ?? null })
  return res.data.data
}
