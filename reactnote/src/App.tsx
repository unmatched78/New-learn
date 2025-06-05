// src/App.tsx
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import PrivateRoute from './components/PrivateRoute';
import LoginPage from './pages/LoginPage';
import NotesPage from './pages/NotesPage';
import RegisterPage from './pages/RegisterPage';
// Import the AuthContext to access user state
import { useAuth } from './context/AuthContext';

function App() {
  const { user, loading } = useAuth();

  // Optionally, if you want to prevent even reaching the login screen
  // if someone is already logged in, you can decide here to redirect from /login → /notes.
  return (
    <BrowserRouter>
      <Routes>
        {/* Public login route */}
        <Route
          path="/login"
          element={
            // If user is already logged in, redirect to /notes
            user ? (
              <Navigate to="/notes" replace />
            ) : (
              <LoginPage />
            )
          }
        />
        {/* for register page */}
        <Route
          path="/register"
          element={
            // If user is already logged in, redirect to /notes
            user ? (
              <Navigate to="/notes" replace />
            ) : (
              <RegisterPage isRegister={true} />
            )
          }/>
        {/* All routes inside <Route element={<PrivateRoute>…</PrivateRoute>}> become protected */}
        <Route
          path="/notes"
          element={
            <PrivateRoute>
              <NotesPage />
            </PrivateRoute>
          }
        />

        {/* You can add more protected routes here:
            <Route path="/profile" element={<PrivateRoute><ProfilePage/></PrivateRoute>} />
            <Route path="/settings" element={<PrivateRoute><SettingsPage/></PrivateRoute>} />
        */}

        {/* If user hits any other path, you might redirect them: */}
        <Route
          path="*"
          element={<Navigate to={user ? '/notes' : '/login'} replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
