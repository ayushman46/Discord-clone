import { create } from 'zustand';

// This defines the structure of our state
interface AuthState {
  token: string | null;
  setToken: (token: string | null) => void;
}

// This creates the actual store
export const useAuthStore = create<AuthState>((set) => ({
  // The initial state: no token because the user isn't logged in.
  token: null,

  // An "action" to update the state.
  setToken: (newToken) => set({ token: newToken }),
}));