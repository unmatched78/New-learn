// src/pages/LoginPage.tsx
import  { useState } from 'react';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useAuth } from '../context/AuthContext';
import { useNavigate, useLocation } from 'react-router-dom';
import { toast } from 'react-hot-toast';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login, loading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // Where the user wanted to go before being redirected to /login
  const from = (location.state as any)?.from?.pathname || '/notes';

  async function handleLogin() {
    if (!username || !password) {
      toast.error('Please enter both username and password.');
      return;
    }

    try {
      await login(username, password);
      // After successful login, go “from” or default to /notes
      navigate(from, { replace: true });
    } catch (err) {
      toast.error('Login failed. Please check your credentials.');
    }
  }

  return (
    <div className="flex items-center justify-center h-screen bg-gray-50">
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle className="text-2xl">Login</CardTitle>
          <CardDescription>
            Enter your credentials to access your notes.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <div className="flex flex-col space-y-4">
            <Input
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <Input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        </CardContent>

        <CardFooter>
          <Button
            className="w-full"
            onClick={handleLogin}
            disabled={loading}
          >
            {loading ? 'Logging in…' : 'Login'}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
