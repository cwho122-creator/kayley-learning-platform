import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const client = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

// Add token to all requests
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default client;
