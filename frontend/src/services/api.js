// frontend/src/services/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000",   // backend URL
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token'); // or from your auth context
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;