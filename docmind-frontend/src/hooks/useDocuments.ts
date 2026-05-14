// src/hooks/useDocuments.ts
import { useState, useCallback } from 'react'
import { listDocuments, uploadDocument, deleteDocument, Document } from '../utils/api'
import toast from 'react-hot-toast'

export function useDocuments() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)

  const fetchDocuments = useCallback(async () => {
    setLoading(true)
    try {
      const docs = await listDocuments()
      setDocuments(docs)
    } catch {
      toast.error('Failed to load documents')
    } finally {
      setLoading(false)
    }
  }, [])

  const upload = useCallback(async (file: File) => {
    setUploading(true)
    try {
      const doc = await uploadDocument(file)
      toast.success(`"${doc.filename}" ingested — ${doc.chunk_count} chunks`)
      await fetchDocuments()
      return doc
    } catch (err: any) {
      const msg = err?.response?.data?.message || 'Upload failed'
      toast.error(msg)
    } finally {
      setUploading(false)
    }
  }, [fetchDocuments])

  const remove = useCallback(async (docId: string) => {
    try {
      await deleteDocument(docId)
      setDocuments(prev => prev.filter(d => d.doc_id !== docId))
      toast.success('Document removed')
    } catch {
      toast.error('Failed to delete document')
    }
  }, [])

  return { documents, loading, uploading, fetchDocuments, upload, remove }
}
