// frontend/src/services/causeService.js
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const API_URL = 'http://localhost:5000/api';

export const login = async (email, password) => {
  const res = await axios.post(`${API_URL}/auth/login`, { email, password });
  return res.data;
};

export const getUserFromToken = (token) => {
  const decoded = jwtDecode(token);
  return { id: decoded.sub, name: decoded.name, role: decoded.role, email: decoded.email };
};

export const getAllCauses = async () => {
  const res = await axios.get(`${API_URL}/causes`);
  return res.data.data;
};

export const getCauseById = async (id) => {
  const res = await axios.get(`${API_URL}/causes/${id}`);
  return res.data;
};