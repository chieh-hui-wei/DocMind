// src/hooks/useChat.ts
import { useState, useCallback } from 'react'
import { askQuestion, ChatAnswer } from '../utils/api'
import toast from 'react-hot-toast'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  sources?: ChatAnswer['sources']
  timestamp: Date
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [thinking, setThinking] = useState(false)

  const sendMessage = useCallback(async (question: string, docId?: string) => {
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: question,
      timestamp: new Date(),
    }
    setMessages(prev => [...prev, userMsg])
    setThinking(true)

    try {
      const result = await askQuestion(question, docId)
      const assistantMsg: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: result.answer,
        sources: result.sources,
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, assistantMsg])
    } catch (err: any) {
      const msg = err?.response?.data?.message || 'Failed to get an answer'
      toast.error(msg)
      const errMsg: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: `_Error: ${msg}_`,
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, errMsg])
    } finally {
      setThinking(false)
    }
  }, [])

  const clearChat = useCallback(() => setMessages([]), [])

  return { messages, thinking, sendMessage, clearChat }
}
