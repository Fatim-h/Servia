import React, { createContext, useContext, useState, useEffect } from "react";
import { loginUser, logoutUser, getCurrentUser } from "../services/authService";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState(null);

  // Load current user on app start
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const user = await getCurrentUser();
        if (user && !user.error) setAuth(user);
        else setAuth(null);
      } catch {
        setAuth(null);
      }
    };
    fetchUser();
  }, []);

  // Login function
  const login = async ({ name, password }) => {
    try {
      const user = await loginUser(name, password);
      if (!user || user.error) return false; // check backend error

      setAuth(user);
      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  };

  // Logout function
  const logout = async () => {
    try {
      await logoutUser();
    } finally {
      setAuth(null);
    }
  };

  return (
    <AuthContext.Provider value={{ auth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);