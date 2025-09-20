import { AxiosError } from 'axios';

export interface SWRHookReturn<T> {
  data?: T;
  isLoading: boolean;
  error?: AxiosError;
}
