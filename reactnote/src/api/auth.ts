// src/api/auth.ts
import api, { storeTokens, clearTokens } from './api';

// 1) Login: call /api/token/ to get { access, refresh }
export interface LoginCredentials {
  username: string;
  password: string;
}

export interface TokenPair {
  access: string;
  refresh: string;
}

export async function loginUser(creds: LoginCredentials): Promise<TokenPair> {
  const response = await api.post<TokenPair>('/api/token/', {
    username: creds.username,
    password: creds.password,
  });
  const { access, refresh } = response.data;
  // Store tokens in localStorage
  storeTokens(access, refresh);
  return { access, refresh };
}

// 2) Logout: just clear tokens on the client side
export function logoutUser() {
  clearTokens();
}

// 3) Optionally, if you have an endpoint to fetch “current user” details:
export interface UserData {
  id: number;
  username: string;
  email: string;
  // …etc (whatever your DRF serializer returns)
}

export async function fetchCurrentUser(): Promise<UserData> {
  const response = await api.get<UserData>('/api/users/me/');
  return response.data;
}
