// src/context/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';
import * as causeService from '../services/causeservice';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  // Load user from localStorage if token exists
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const loggedUser = causeService.getUserFromToken(token);
      setUser(loggedUser);
    }
  }, []);

  const login = async (email, password) => {
    try {
      const data = await causeService.login(email, password);
      localStorage.setItem('token', data.token);
      const loggedUser = causeService.getUserFromToken(data.token);
      setUser(loggedUser);
      return loggedUser;
    } catch (err) {
      throw err;
    }
  };

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