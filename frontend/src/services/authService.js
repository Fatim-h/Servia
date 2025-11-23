// src/services/authService.js
import api from "./api";

// LOGIN
export const loginUser = async (email, password) => {
  try {
    const response = await api.post("/api/auth/login", { name: email, password });
    return response.data;
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

// GET USER FROM TOKEN
export const getUserFromToken = async (token) => {
  try {
    const response = await api.get("/api/auth/user", {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: "Failed to fetch user" };
  }
};