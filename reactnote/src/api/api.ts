// src/api/api.ts
//import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import axios, { AxiosError } from "axios";
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";//compatibilty with docker
// 1) Create an Axios instance with your Django DRF backend base URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

// 2) Helper to read/write tokens from localStorage (or sessionStorage)
const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

export function getStoredAccessToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getStoredRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function storeTokens(access: string, refresh: string) {
  localStorage.setItem(ACCESS_TOKEN_KEY, access);
  localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

// 3) Request interceptor: attach access token to every request
import type { InternalAxiosRequestConfig } from "axios";

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = getStoredAccessToken();
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    // TS now understands you're returning an InternalAxiosRequestConfig
    return config;
  },
  (error) => Promise.reject(error)
);


// 4) Response interceptor: if we get a 401 (access expired), try to refresh
let isRefreshing = false;
let failedQueue: Array<{
  resolve: (value?: AxiosResponse<any>) => void;
  reject: (error: any) => void;
  config: AxiosRequestConfig;
}> = [];

function processQueue(error: any, token: string | null = null) {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.config.headers = prom.config.headers || {};
      if (token) {
        prom.config.headers.Authorization = `Bearer ${token}`;
      }
      prom.resolve(api(prom.config));
    }
  });
  failedQueue = [];
}

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config!;
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      getStoredRefreshToken()
    ) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject, config: originalRequest });
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const refreshToken = getStoredRefreshToken()!;
        // ← changed from "/api/token/refresh/" to "/token/refresh/"
        const { data } = await api.post("/token/refresh/", {
          refresh: refreshToken,
        });

        const newAccessToken = data.access;
        localStorage.setItem(ACCESS_TOKEN_KEY, newAccessToken);
        processQueue(null, newAccessToken);
        isRefreshing = false;

        originalRequest.headers = originalRequest.headers || {};
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        isRefreshing = false;
        clearTokens();
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
