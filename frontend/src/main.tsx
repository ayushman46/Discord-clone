import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import './index.css';

import LoginPage from './pages/loginpage';
import RegisterPage from './pages/registerpage';
import MainAppPage from './pages/mainapppage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainAppPage />,
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