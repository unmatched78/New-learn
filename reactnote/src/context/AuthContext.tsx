// src/context/AuthContext.tsx
import React, {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from 'react';
import { 
  loginUser, 
  logoutUser as apiLogout, 
  fetchCurrentUser, 
  TokenPair, 
  UserData 
} from '../api/auth';
import { getStoredAccessToken, getStoredRefreshToken, clearTokens } from '../api/api';

interface AuthContextType {
  user: UserData | null;
  accessToken: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<UserData | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(getStoredAccessToken());
  const [loading, setLoading] = useState<boolean>(true);

  // 1) On mount, if there's an access token in localStorage, try to fetch current user
  useEffect(() => {
    async function initialize() {
      const token = getStoredAccessToken();
      const refresh = getStoredRefreshToken();

      if (token && refresh) {
        try {
          const data = await fetchCurrentUser();
          setUser(data);
          setAccessToken(token);
        } catch (e) {
          // If fetchCurrentUser fails (e.g. token expired), clear everything
          clearTokens();
          setUser(null);
          setAccessToken(null);
        }
      }
      setLoading(false);
    }
    initialize();
  }, []);

  // 2) login(): call API, store tokens, fetch user, update state
  async function login(username: string, password: string) {
    setLoading(true);
    try {
      const { access, refresh }: TokenPair = await loginUser({ username, password });
      setAccessToken(access);
      // Now that we have an accessToken, fetch user details
      const userData = await fetchCurrentUser();
      setUser(userData);
    } catch (err) {
      // propagate error to UI
      setUser(null);
      setAccessToken(null);
      throw err;
    } finally {
      setLoading(false);
    }
  }

  // 3) logout(): clear tokens + state, call any API logout if needed
  function logout() {
    apiLogout(); // just clears localStorage
    setUser(null);
    setAccessToken(null);
  }

  const value: AuthContextType = {
    user,
    accessToken,
    login,
    logout,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
