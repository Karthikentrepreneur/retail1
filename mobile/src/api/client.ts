import axios from 'axios';

export const apiClient = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_BASE_URL || 'http://10.0.2.2:8000/api',
  timeout: 5000
});

apiClient.interceptors.request.use((config) => {
  const token = ''; // integrate secure storage later
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
