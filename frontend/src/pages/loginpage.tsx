import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export default function LoginPage() {
  const navigate = useNavigate();
  // Get the setToken function from our global auth store (the "notice board")
  const setToken = useAuthStore((state) => state.setToken);

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // IMPORTANT: The /token endpoint expects "form data", not JSON.
    // We create a FormData object to send the credentials.
    const formData = new FormData();
    formData.append('username', email); // The backend expects the email in the 'username' field
    formData.append('password', password);

    try {
      // Send the form data to the /token endpoint
      const response = await axios.post('http://127.0.0.1:8000/token', formData);

      // If login is successful, get the token from the response
      const accessToken = response.data.access_token;

      // Save the token to our global store
      setToken(accessToken);

      // Redirect the user to the main application page
      navigate('/');
    } catch (err: any) {
      if (axios.isAxiosError(err) && err.response) {
        setError(err.response.data.detail || 'Login failed.');
      } else {
        setError('An unexpected error occurred.');
      }
    }
  };

  return (
    <div className="bg-gray-900 text-white h-screen flex items-center justify-center">
      <div className="w-full max-w-md p-8 space-y-6 bg-gray-800 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center">Welcome Back</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="bg-gray-700 border-gray-600"
            />
          </div>
          <div>
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="bg-gray-700 border-gray-600"
            />
          </div>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <Button type="submit" className="w-full">
            Login
          </Button>
        </form>
      </div>
    </div>
  );
}