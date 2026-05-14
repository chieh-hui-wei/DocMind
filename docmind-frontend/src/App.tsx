// src/App.tsx
import { useEffect, useRef, useState } from 'react'
import { Toaster } from 'react-hot-toast'
import { useDropzone } from 'react-dropzone'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import {
  FileText, Trash2, Upload, Send, Brain,
  ChevronDown, X, BookOpen, Sparkles, RotateCcw,
  ExternalLink, Loader2,
} from 'lucide-react'
import { useDocuments } from './hooks/useDocuments'
import { useChat } from './hooks/useChat'
import { Document } from './utils/api'
import './styles/app.css'

export default function App() {
  const { documents, loading, uploading, fetchDocuments, upload, remove } = useDocuments()
  const { messages, thinking, sendMessage, clearChat } = useChat()
  const [question, setQuestion] = useState('')
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null)
  const [activeSource, setActiveSource] = useState<number | null>(null)
  const bottomRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => { fetchDocuments() }, [fetchDocuments])
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, thinking])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: async ([file]) => { if (file) await upload(file) },
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'text/markdown': ['.md'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    multiple: false,
  })

  const handleSend = async () => {
    const q = question.trim()
    if (!q || thinking) return
    setQuestion('')
    await sendMessage(q, selectedDoc?.doc_id)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="app">
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: 'var(--ink-3)',
            color: 'var(--loud)',
            border: '1px solid var(--border)',
            fontFamily: 'var(--font-mono)',
            fontSize: '13px',
          },
        }}
      />

      {/* ── Sidebar ───────────────────────────────────────────────────────────── */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <Brain className="logo-icon" size={22} />
          <span className="logo-text">DocMind</span>
        </div>

        {/* Upload zone */}
        <div
          {...getRootProps()}
          className={`dropzone ${isDragActive ? 'drag-active' : ''} ${uploading ? 'uploading' : ''}`}
        >
          <input {...getInputProps()} />
          {uploading ? (
            <><Loader2 size={18} className="spin" /><span>Processing…</span></>
          ) : isDragActive ? (
            <><Upload size={18} /><span>Drop it</span></>
          ) : (
            <><Upload size={18} /><span>Upload document</span></>
          )}
          <p className="dropzone-hint">PDF · DOCX · TXT · MD</p>
        </div>

        {/* Document list */}
        <div className="doc-list-header">
          <BookOpen size={13} />
          <span>Knowledge Base</span>
          {loading && <Loader2 size={12} className="spin muted" />}
        </div>

        <ul className="doc-list">
          {documents.length === 0 && !loading && (
            <li className="doc-empty">No documents yet</li>
          )}
          {documents.map(doc => (
            <li
              key={doc.doc_id}
              className={`doc-item ${selectedDoc?.doc_id === doc.doc_id ? 'active' : ''}`}
              onClick={() => setSelectedDoc(prev => prev?.doc_id === doc.doc_id ? null : doc)}
            >
              <FileText size={13} className="doc-icon" />
              <span className="doc-name" title={doc.filename}>{doc.filename}</span>
              <button
                className="doc-delete"
                onClick={e => { e.stopPropagation(); remove(doc.doc_id) }}
                title="Remove"
              >
                <Trash2 size={12} />
              </button>
            </li>
          ))}
        </ul>

        <div className="sidebar-footer">
          <span>FastAPI · ChromaDB · Claude</span>
        </div>
      </aside>

      {/* ── Main ─────────────────────────────────────────────────────────────── */}
      <main className="main">

        {/* Topbar */}
        <header className="topbar">
          <div className="topbar-left">
            {selectedDoc ? (
              <span className="scope-badge">
                <FileText size={12} />
                Scoped: {selectedDoc.filename}
                <button onClick={() => setSelectedDoc(null)}><X size={11} /></button>
              </span>
            ) : (
              <span className="scope-all">All documents</span>
            )}
          </div>
          <div className="topbar-right">
            {messages.length > 0 && (
              <button className="btn-ghost" onClick={clearChat}>
                <RotateCcw size={14} /> Clear
              </button>
            )}
          </div>
        </header>

        {/* Messages */}
        <div className="messages">
          {messages.length === 0 && (
            <div className="empty-state">
              <Sparkles size={36} className="empty-icon" />
              <h2>Ask anything about your documents</h2>
              <p>Upload a PDF, DOCX, TXT, or MD file on the left,<br />then ask a question here.</p>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={msg.id} className={`message ${msg.role}`}>
              <div className="message-bubble">
                {msg.role === 'assistant' ? (
                  <div className="markdown-content">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                ) : (
                  <p>{msg.content}</p>
                )}
              </div>

              {/* Sources */}
              {msg.sources && msg.sources.length > 0 && (
                <div className="sources">
                  <button
                    className="sources-toggle"
                    onClick={() => setActiveSource(activeSource === i ? null : i)}
                  >
                    <ExternalLink size={11} />
                    {msg.sources.length} source{msg.sources.length > 1 ? 's' : ''}
                    <ChevronDown size={11} className={activeSource === i ? 'rotated' : ''} />
                  </button>
                  {activeSource === i && (
                    <ul className="source-list">
                      {msg.sources.map((s, j) => (
                        <li key={j} className="source-item">
                          <div className="source-meta">
                            <FileText size={11} />
                            <span>{s.filename ?? 'unknown'}</span>
                            <span className="source-score">{(s.score * 100).toFixed(0)}%</span>
                          </div>
                          <p className="source-excerpt">{s.excerpt}</p>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              )}
            </div>
          ))}

          {thinking && (
            <div className="message assistant">
              <div className="message-bubble thinking">
                <span /><span /><span />
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="input-area">
          <div className="input-box">
            <textarea
              ref={inputRef}
              value={question}
              onChange={e => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={documents.length === 0 ? 'Upload a document first…' : 'Ask a question… (Enter to send)'}
              disabled={documents.length === 0 || thinking}
              rows={1}
            />
            <button
              className="send-btn"
              onClick={handleSend}
              disabled={!question.trim() || thinking || documents.length === 0}
            >
              {thinking ? <Loader2 size={16} className="spin" /> : <Send size={16} />}
            </button>
          </div>
          <p className="input-hint">
            {selectedDoc
              ? `Searching within "${selectedDoc.filename}" only`
              : 'Searching all documents · Shift+Enter for new line'}
          </p>
        </div>
      </main>
    </div>
  )
}
