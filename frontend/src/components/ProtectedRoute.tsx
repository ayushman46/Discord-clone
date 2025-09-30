import { useAuthStore } from '@/stores/authStore';
import { Navigate, Outlet } from 'react-router-dom';

export default function ProtectedRoute() {
  // Get the token from our global "notice board"
  const token = useAuthStore((state) => state.token);

  // If there is a token, the user is logged in.
  // The <Outlet /> component will render the actual page (e.g., MainAppPage).
  if (token) {
    return <Outlet />;
  }

  // If there is no token, redirect the user to the login page.
  return <Navigate to="/login" />;
}