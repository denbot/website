import type { AxiosResponse } from 'axios';

import { AuthStatus } from '@/models/auth-flow-response.model';

import { axiosInstance } from './axios';

async function login(phoneNumber: string): Promise<AuthStatus> {
  try {
    const { data }: AxiosResponse<{ status: AuthStatus }> =
      await axiosInstance.post('/auth/login', { phoneNumber });
    return data.status ?? 'error';
  } catch {
    return 'error';
  }
}

async function loginOtp(phoneNumber: string, otp: string): Promise<AuthStatus> {
  try {
    const { data }: AxiosResponse<{ status: AuthStatus }> =
      await axiosInstance.post('/auth/login_otp', {
        phoneNumber,
        verificationCode: otp,
      });
    return data.status ?? 'error';
  } catch {
    return 'error';
  }
}

export { login, loginOtp };
