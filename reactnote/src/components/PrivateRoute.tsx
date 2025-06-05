// src/components/PrivateRoute.tsx
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface PrivateRouteProps {
  children: JSX.Element;
}

/**
 * PrivateRoute checks:
 *   1) If auth is still loading → show a simple "loading" placeholder (you can swap in a spinner).
 *   2) If no user → redirect to /login (preserving "from" location so you can return after login if desired).
 *   3) Otherwise → render children.
 */
export default function PrivateRoute({ children }: PrivateRouteProps) {
  const { user, loading } = useAuth();
  const location = useLocation();

  // 1) While AuthContext is determining if there's an existing token & fetching /user → show loading
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-gray-500">Loading…</p>
      </div>
    );
  }

  // 2) If there's no authenticated user, redirect to /login
  if (!user) {
    // ⇢ We pass along state={{ from: location }} so you can read it in the login page
    //    and navigate back to where the user originally wanted to go after successful login.
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // 3) Otherwise, render the protected children
  return children;
}

// Note: You can customize the loading placeholder or redirect behavior as needed.
//       This is a simple example to demonstrate the concept.