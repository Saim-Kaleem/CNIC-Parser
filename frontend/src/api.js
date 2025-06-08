import axios from 'axios';

const API_BASE = 'http://localhost:5000';

export const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append('image', file);

  const res = await axios.post(`${API_BASE}/parse`, formData);
  return res.data;
};