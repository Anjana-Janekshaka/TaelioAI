"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';

interface User {
  id: string;
  email: string;
  role: string;
  tier?: string;
  limits?: Record<string, any>;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (userData: User) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on mount
    const checkAuth = () => {
      try {
        const token = localStorage.getItem('auth_token');
        const userId = localStorage.getItem('user_id');
        const userEmail = localStorage.getItem('user_email');
        const userRole = localStorage.getItem('user_role');
        const userTier = localStorage.getItem('user_tier');
        const userLimits = localStorage.getItem('user_limits');

        if (token && userId && userEmail && userRole) {
          setUser({
            id: userId,
            email: userEmail,
            role: userRole,
            tier: userTier || undefined,
            limits: userLimits ? JSON.parse(userLimits) : undefined
          });
        }
      } catch (error) {
        console.error('Error checking auth:', error);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = (userData: User) => {
    setUser(userData);
  };

  const logout = () => {
    // Clear localStorage
    localStorage.removeItem('auth_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_email');
    localStorage.removeItem('user_role');
    localStorage.removeItem('user_tier');
    localStorage.removeItem('user_limits');
    
    // Clear user state
    setUser(null);
  };

  const isAuthenticated = !!user;

  return (
    <AuthContext.Provider value={{
      user,
      isLoading,
      login,
      logout,
      isAuthenticated
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
