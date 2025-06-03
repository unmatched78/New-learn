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
    (error) => {
        console.error('API error:', {
            message: error.message,
            response: error.response?.data,
            status: error.response?.status
        })
        return Promise.reject(error)
    }
)

export default api