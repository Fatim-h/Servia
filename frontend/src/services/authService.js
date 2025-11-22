// src/services/authService.js
import api from "./api";

export const loginUser = async (name, password) => {
  try {
    const response = await api.post("/api/login", { name, password });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: "Login failed" };
  }
};

export const registerUser = async (data) => {
  try {
    const response = await api.post("/api/register", data);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: "Registration failed" };
  }
};