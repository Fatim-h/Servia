// src/services/authService.js
import api from "./api";

// LOGIN using session cookie
export const loginUser = async (name, password) => {
  try {
    const response = await api.post("/api/auth/login", { name, password });
    return response.data; // { auth_id, role, name } from backend session
  } catch (error) {
    throw error.response?.data || { error: "Login failed" };
  }
};

// REGISTER
export const registerUser = async (data) => {
  try {
    const response = await api.post("/api/auth/register", data);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: "Registration failed" };
  }
};

// LOGOUT
export const logoutUser = async () => {
  try {
    await api.post("/api/auth/logout"); // optional backend logout endpoint
    return true;
  } catch (error) {
    throw error.response?.data || { error: "Logout failed" };
  }
};

// GET CURRENT USER (from session)
export const getCurrentUser = async () => {
  try {
    const response = await api.get("/api/auth/user"); // returns session user info
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: "Failed to fetch user" };
  }
};