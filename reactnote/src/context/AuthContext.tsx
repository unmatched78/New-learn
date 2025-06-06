// src/context/AuthContext.tsx
import {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from 'react';
import {
  loginUser,
  registerUser,
  logoutUser as apiLogout,
  fetchCurrentUser,
  UserData,
} from '../api/auth';
import { getStoredAccessToken, getStoredRefreshToken, clearTokens } from '../api/api';

interface AuthContextType {
  user: UserData | null;
  accessToken: string | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string) => Promise<void>;
  logout: () => void;
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
  const [accessToken, setAccessToken] = useState<string | null>(
    getStoredAccessToken()
  );
  const [loading, setLoading] = useState<boolean>(true);

  // 1) On mount, if tokens exist, try to fetchCurrentUser
  useEffect(() => {
    async function initialize() {
      const token = getStoredAccessToken();
      const refresh = getStoredRefreshToken();
      if (token && refresh) {
        try {
          const data = await fetchCurrentUser();
          setUser(data);
          setAccessToken(token);
        } catch {
          clearTokens();
          setUser(null);
          setAccessToken(null);
        }
      }
      setLoading(false);
    }
    initialize();
  }, []);

  // 2) login(): call loginUser(), then fetchCurrentUser()
  async function login(username: string, password: string) {
    setLoading(true);
    try {
      const { access } = await loginUser({ username, password });
      setAccessToken(access);
      const userData = await fetchCurrentUser();
      setUser(userData);
    } catch (err) {
      setUser(null);
      setAccessToken(null);
      throw err;
    } finally {
      setLoading(false);
    }
  }

  // 3) register(): call registerUser(), then fetchCurrentUser()
  async function register(username: string, password: string) {
    setLoading(true);
    try {
      const { access } = await registerUser({ username, password });
      setAccessToken(access);
      const userData = await fetchCurrentUser();
      setUser(userData);
    } catch (err) {
      setUser(null);
      setAccessToken(null);
      throw err;
    } finally {
      setLoading(false);
    }
  }

  // 4) logout(): clear tokens + context state
  function logout() {
    apiLogout();
    setUser(null);
    setAccessToken(null);
  }

  const value: AuthContextType = {
    user,
    accessToken,
    loading,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
