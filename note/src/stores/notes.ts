import { defineStore } from 'pinia'
import api from '../api'
import type { AxiosError } from 'axios'

interface Note {
  id: number
  content: string
  created_at: string
  updated_at: string
  notewriter: { id: number; username: string; role: string } | null
}

interface ErrorResponse {
  error?: { message: string; details: any }
}

export const useNotesStore = defineStore('notes', {
  state: () => ({
    notes: [] as Note[],
  }),
  actions: {
    async fetchNotes() {
      try {
        const response = await api.get<Note[]>('/notes/')
        this.notes = response.data
      } catch (error) {
        const err = error as AxiosError<ErrorResponse>
        throw err.response?.data?.error || { message: 'Failed to fetch notes' }
      }
    },
    async createNote(content: string) {
      try {
        const response = await api.post<Note>('/notes/', { content })
        this.notes.push(response.data)
      } catch (error) {
        const err = error as AxiosError<ErrorResponse>
        throw err.response?.data?.error || { message: 'Failed to create note' }
      }
    },
    async updateNote(id: number, content: string) {
      try {
        const response = await api.put<Note>(`/notes/${id}/`, { content })
        const index = this.notes.findIndex((note) => note.id === id)
        if (index !== -1) {
          this.notes[index] = response.data
        }
      } catch (error) {
        const err = error as AxiosError<ErrorResponse>
        throw err.response?.data?.error || { message: 'Failed to update note' }
      }
    },
    async deleteNote(id: number) {
      try {
        await api.delete(`/notes/${id}/`)
        this.notes = this.notes.filter((note) => note.id !== id)
      } catch (error) {
        const err = error as AxiosError<ErrorResponse>
        throw err.response?.data?.error || { message: 'Failed to delete note' }
      }
    },
  },
})