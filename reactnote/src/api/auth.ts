// src/api/auth.ts
import api, { storeTokens, clearTokens } from "./api";

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface TokenPair {
  access: string;
  refresh: string;
}

// (Optional) shape of the user object your backend returns
export interface UserData {
  id: number;
  username: string;
  role: string;
  // …any other fields you need
}

// ─── 1) LOGIN: POST /api/auth/token/login/ ───────────────────────────────────────
export async function loginUser(
  creds: LoginCredentials
): Promise<TokenPair> {
  // Note: if VITE_API_BASE_URL = "http://localhost:8000/api",
  // then this actually POSTs to "http://localhost:8000/api/auth/token/login/"
  const response = await api.post<{
    tokens: { access: string; refresh: string };
    user: any;
  }>("/auth/token/login/", {
    username: creds.username,
    password: creds.password,
  });

  const { access, refresh } = response.data.tokens;
  storeTokens(access, refresh);
  return { access, refresh };
}

// ─── 2) REGISTER: POST /api/register/ ────────────────────────────────────────────
export async function registerUser(
  creds: LoginCredentials
): Promise<TokenPair> {
  // If your DRF RegisterView returns { tokens: { access, refresh }, user: { … } }
  const response = await api.post<{
    tokens: { access: string; refresh: string };
    user: any;
  }>("/register/", {
    username: creds.username,
    password: creds.password,
  });

  const { access, refresh } = response.data.tokens;
  storeTokens(access, refresh);
  return { access, refresh };
}

// ─── 3) LOGOUT: just clear tokens on client ───────────────────────────────────────
export function logoutUser() {
  clearTokens();
}

// ─── 4) FETCH CURRENT USER: GET /api/users/me/ ───────────────────────────────────
export async function fetchCurrentUser(): Promise<UserData> {
  // Be sure you add a “/api/users/me/” URL on the Django side (see below).
  const response = await api.get<UserData>("/users/me/");
  return response.data;
}
