// src/pages/RegisterPage.tsx
import { useState } from 'react';
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

export default function RegisterPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { register, loading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // If someone was redirected here, 
  // location.state.from.pathname tells us where to go after registering.
  const from = (location.state as any)?.from?.pathname || '/notes';

  async function handleRegister() {
    if (!username || !password) {
      toast.error('Please enter both username and password.');
      return;
    }

    try {
      await register(username, password);
      navigate(from, { replace: true });
    } catch (err) {
      toast.error('Registration failed. Please try again.');
    }
  }

  return (
    <div className="flex items-center justify-center h-screen bg-gray-50">
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle className="text-2xl">Register</CardTitle>
          <CardDescription>Create a new account to access your notes.</CardDescription>
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
            onClick={handleRegister}
            disabled={loading}
          >
            {loading ? 'Registering…' : 'Register'}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
