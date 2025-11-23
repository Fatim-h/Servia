// src/services/causeService.js
import api from "./api";

// GET all verified causes (NGOs + Events)
export const getAllCauses = async () => {
  try {
    const response = await api.get("/api/causes");
    return response.data; // { causes: [...] }
  } catch (error) {
    console.error("Error fetching causes:", error);
    throw error.response?.data || { error: "Failed to fetch causes" };
  }
};

// GET a single cause by ID
export const getCauseById = async (cause_id) => {
  try {
    const response = await api.get(`/api/causes/${cause_id}`);
    return response.data; // single cause object
  } catch (error) {
    console.error(`Error fetching cause ${cause_id}:`, error);
    throw error.response?.data || { error: "Failed to fetch cause" };
  }
};