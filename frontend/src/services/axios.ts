import axios, { type AxiosInstance } from 'axios';
import toast from 'react-hot-toast';

export const axiosInstance: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 1000,
});

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const status = error.response.status;
      const message =
        error.response.data?.reason || error.response.data?.message || null;

      if (status === 401) {
        toast.error('You need to log in.');
      } else if (status === 403) {
        toast.error("You don't have permission to do that.");
      } else if (status >= 500) {
        toast.error('Server error. Try again later.');
      } else if (message) {
        toast.error(message);
      }
    } else if (error.request) {
      toast.error('No response from server.');
    } else {
      toast.error('Request setup error.');
    }

    return Promise.reject(error);
  },
);
