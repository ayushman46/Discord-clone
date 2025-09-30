import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import './index.css';

import LoginPage from './pages/loginpage';
import RegisterPage from './pages/registerpage';
import MainAppPage from './pages/mainapppage';
import ProtectedRoute from './components/ProtectedRoute'; // <-- Import the lock

const router = createBrowserRouter([
  {
    // This is the parent route that uses our lock
    element: <ProtectedRoute />,
    children: [
      {
        path: '/',
        element: <MainAppPage />,
      },
      // You can add more protected routes here later
    ],
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/register',
    element: <RegisterPage />,
  },
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);