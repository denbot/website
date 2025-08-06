import axios, { AxiosInstance } from 'axios';

export const axiosInstance: AxiosInstance = axios.create({
  baseURL: process.env.BACKEND_BASE_URL,
  timeout: 1000,
});
