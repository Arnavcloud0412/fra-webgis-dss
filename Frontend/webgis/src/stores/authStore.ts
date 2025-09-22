import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { api } from '../services/api';

interface User {
  id: number;
  username: string;
  email: string;
  role: string;
  created_at: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  register: (username: string, email: string, password: string) => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (username: string, password: string) => {
        try {
          const response = await api.post('/auth/login', { username, password });
          const { access_token, user } = response.data;
          
          set({
            user,
            token: access_token,
            isAuthenticated: true,
          });
          
          // Set token in API headers
          api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        } catch (error: any) {
          throw new Error(error.response?.data?.error || 'Login failed');
        }
      },

      register: async (username: string, email: string, password: string) => {
        try {
          const response = await api.post('/auth/register', { 
            username, 
            email, 
            password 
          });
          const { access_token, user } = response.data;
          
          set({
            user,
            token: access_token,
            isAuthenticated: true,
          });
          
          // Set token in API headers
          api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        } catch (error: any) {
          throw new Error(error.response?.data?.error || 'Registration failed');
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
        
        // Remove token from API headers
        delete api.defaults.headers.common['Authorization'];
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
