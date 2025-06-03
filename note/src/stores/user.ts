import { defineStore } from 'pinia'
import api from '../api'
import type { AxiosError } from 'axios'

interface User {
  id: number
  username: string
  role: string
}

interface AuthResponse {
  tokens: { access: string; refresh: string }
  user: User
}

interface ErrorResponse {
  error?: { message: string; details: any }
}

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    accessToken: null as string | null,
    refreshToken: null as string | null,
  }),
  actions: {
    async login(credentials: { username: string; password: string }) {
      try {
        const response = await api.post<AuthResponse>('/auth/token/login/', credentials)
        this.user = response.data.user
        this.accessToken = response.data.tokens.access
        this.refreshToken = response.data.tokens.refresh
        localStorage.setItem('access_token', this.accessToken)
        localStorage.setItem('refresh_token', this.refreshToken)
        api.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
      } catch (error) {
        const err = error as AxiosError<ErrorResponse>
        throw err.response?.data?.error || { message: 'Login failed' }
      }
    },
    async register(data: { username: string; password: string; password2: string; role: string }) {
      try {
        const response = await api.post<AuthResponse>('/register/', data)
        this.user = response.data.user
        this.accessToken = response.data.tokens.access
        this.refreshToken = response.data.tokens.refresh
        localStorage.setItem('access_token', this.accessToken)
        localStorage.setItem('refresh_token', this.refreshToken)
        api.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
      } catch (error) {
        const err = error as AxiosError<ErrorResponse>
        throw err.response?.data?.error || { message: 'Registration failed' }
      }
    },
    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      delete api.defaults.headers.common['Authorization']
    },
  },
})