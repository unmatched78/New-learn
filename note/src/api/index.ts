import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    console.log('API request:', config.method, config.url, 'Token:', token)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('Request interceptor error:', error)
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => {
    console.log('API response:', response.status, response.data)
    return response
  },
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry === true
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        })
        const newAccessToken = response.data.access
        localStorage.setItem('access_token', newAccessToken)
        api.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`
        return api(originalRequest)
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError)
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
      }
    }
    console.error('API error:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
    })
    return Promise.reject(error)
  }
)

export default api