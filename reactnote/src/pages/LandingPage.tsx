// src/pages/LandingPage.tsx
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import { ModeToggle } from '@/components/mode-toggle';
export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="flex items-center justify-center h-screen ">
      
      <ModeToggle className="absolute top-4 right-4" />

      <div className="text-center space-y-6">
        <h1 className="text-5xl font-extrabold">Welcome to ReactNote</h1>
        <p className="text-xl text-gray-600">
          Your personal note-taking app built for you!
        </p>
        <div className="space-x-4">
          <Button
            onClick={() => navigate('/login')}
            size="lg"
          >
            Login
          </Button>
          <Button
            variant="outline"
            onClick={() => navigate('/register')}
            size="lg"
          >
            Register
          </Button>
        </div>
      </div>
      <footer className="absolute bottom-4 text-sm text-gray-500">
        <p>
          &copy; {new Date().getFullYear()} ReactNote. All rights reserved.
        </p>
      </footer>
    </div>
  );
}
