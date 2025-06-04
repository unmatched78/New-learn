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
        console.log('Fetching notes with token:', localStorage.getItem('access_token'))
        const response = await api.get<Note[]>('/notes/')
        console.log('Fetch response:', response.status, response.data)
        this.notes = response.data
        console.log('Updated notes:', this.notes)
      } catch (error) {
        const err = error as AxiosError<ErrorResponse>
        console.error('Fetch error:', {
          message: err.message,
          response: err.response?.data,
          status: err.response?.status,
        })
        throw err.response?.data?.error || { message: 'Failed to fetch notes' }
      }
    },
    async createNote(content: string) {
      try {
        console.log('Creating note:', content)
        const response = await api.post<Note>('/notes/', { content })
        console.log('Created note:', response.data)
        await this.fetchNotes()
      } catch (error) {
        const err = error as AxiosError<ErrorResponse>
        console.error('Create error:', err.response?.data || err.message)
        throw err.response?.data?.error || { message: 'Failed to create note' }
      }
    },
    async updateNote(id: number, content: string) {
      try {
        console.log('Updating note ID:', id)
        const response = await api.put<Note>(`/notes/${id}/`, { content })
        console.log('Updated note:', response.data)
        await this.fetchNotes()
      } catch (error) {
        const err = error as AxiosError<ErrorResponse>
        console.error('Update error:', err.response?.data || err.message)
        throw err.response?.data?.error || { message: 'Failed to update note' }
      }
    },
    async deleteNote(id: number) {
      try {
        console.log('Deleting note ID:', id)
        await api.delete(`/notes/${id}/`)
        console.log('Deleted note ID:', id)
        await this.fetchNotes()
      } catch (error) {
        const err = error as AxiosError<ErrorResponse>
        console.error('Delete error:', err.response?.data || err.message)
        throw err.response?.data?.error || { message: 'Failed to delete note' }
      }
    },
  },
})