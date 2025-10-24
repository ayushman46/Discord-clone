import { create } from 'zustand';

// This defines the structure of our state
interface AuthState {
  token: string | null;
  setToken: (token: string | null) => void;
  getAuthHeader: () => { Authorization?: string };
}

// This creates the actual store
export const useAuthStore = create<AuthState>((set, get) => ({
  // The initial state: load token from localStorage if available
  token: typeof localStorage !== 'undefined' ? localStorage.getItem('token') : null,

  // An "action" to update the state and persist to localStorage
  setToken: (newToken) => {
    set({ token: newToken });
    if (typeof localStorage !== 'undefined') {
      if (newToken) {
        localStorage.setItem('token', newToken);
      } else {
        localStorage.removeItem('token');
      }
    }
  },

  // Helper to get Authorization header
  getAuthHeader: () => {
    const token = get().token;
    return token ? { Authorization: `Bearer ${token}` } : {};
  },
}));