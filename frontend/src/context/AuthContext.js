import React, { createContext, useContext, useState } from 'react';
import api from '../services/api'; // Axios instance with baseURL

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState(() => {
    const stored = localStorage.getItem('auth');
    return stored ? JSON.parse(stored) : null;
  });

  // Login function
  const login = async ({ name, password }) => {
    try {
      const res = await api.post('/api/auth/login', { name, password });
      const data = res.data;

      const authData = {
        token: data.token,
        authId: data.auth_id,  // renamed for clarity
        role: data.role,
        name: data.name,
      };

      setAuth(authData);
      localStorage.setItem('auth', JSON.stringify(authData));
      return true;
    } catch (err) {
      console.error(err.response?.data || err);
      alert(err.response?.data?.error || 'Login failed');
      return false;
    }
  };

  const logout = () => {
    setAuth(null);
    localStorage.removeItem('auth');
  };

  return (
    <AuthContext.Provider value={{ auth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);