
import axios from 'axios';

const API_URL = 'https://zl2pcttxj4.execute-api.eu-central-1.amazonaws.com/dev';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false
});

export const classifyImage = async (base64Image: string) => {
  try {
    const response = await api.post('/classify', {
      image: base64Image,
    });
    return response.data;
  } catch (error) {
    console.error('Error in image classification:', error);
    throw error;
  }
};

export default api; 