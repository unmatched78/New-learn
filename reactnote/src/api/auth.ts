// src/api/auth.ts
import api, { storeTokens, clearTokens } from './api';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface TokenPair {
  access: string;
  refresh: string;
}

export interface UserData {
  id: number;
  username: string;
  email?: string;
  // …any other fields your DRF serializer returns
}

// 1) Login: POST /api/token/ → { access, refresh }
export async function loginUser(
  creds: LoginCredentials
): Promise<TokenPair> {
  const response = await api.post<TokenPair>('/api/token/', {
    username: creds.username,
    password: creds.password,
  });
  const { access, refresh } = response.data;
  storeTokens(access, refresh);
  return { access, refresh };
}

// 2) Register: POST /api/register/ → { access, refresh } (or just a success message)
//    Here we assume registration endpoint returns tokens directly. If yours only returns
//    a user object, you can then call loginUser() afterward.
export async function registerUser(
  creds: LoginCredentials
): Promise<TokenPair> {
  // Adjust this URL if your DRF URL is something like /api/users/register/ or similar
  const response = await api.post<TokenPair>('/api/register/', {
    username: creds.username,
    password: creds.password,
  });

  // If your backend returns { access, refresh } right away:
  const { access, refresh } = response.data;
  storeTokens(access, refresh);
  return { access, refresh };

  // If your backend only returns a “user created” message, do this instead:
  // await api.post('/api/register/', { username: creds.username, password: creds.password });
  // return loginUser(creds);
}

// 3) Logout: just clear tokens on client side
export function logoutUser() {
  clearTokens();
}

// 4) Fetch current user: GET /api/users/me/ (protected by JWTAuthentication)
export async function fetchCurrentUser(): Promise<UserData> {
  const response = await api.get<UserData>('/api/users/me/');
  return response.data;
}
