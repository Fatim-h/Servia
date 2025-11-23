// src/context/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';
import * as authService from '../services/authService';
import { getUserFromToken } from '../services/authService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setUser(getUserFromToken(token));
    }
  }, []);

  // LOGIN
  const login = async (email, password) => {
    try {
      const data = await authService.loginUser(email, password); // returns { token }
      localStorage.setItem('token', data.token);

      const decoded = getUserFromToken(data.token);
      setUser(decoded);
      return decoded;
    } catch (err) {
      throw err;
    }
  };

  // LOGOUT
  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);