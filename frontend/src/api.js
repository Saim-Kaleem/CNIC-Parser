import axios from 'axios';

// Environment-aware API configuration
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append('image', file);

  const res = await axios.post(`${API_BASE}/parse`, formData);
  return res.data;
};