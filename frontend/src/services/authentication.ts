import { AuthStatus } from '@/models/auth-flow-response.model';
import { AxiosResponse } from 'axios';

import { axiosInstance } from './axios';

async function login(phoneNumber: string): Promise<AuthStatus> {
  const { data }: AxiosResponse<{ status: AuthStatus }> =
    await axiosInstance.post('/auth/login', { phoneNumber });
  return data.status;
}

async function loginOtp(phoneNumber: string, otp: string): Promise<AuthStatus> {
  const { data }: AxiosResponse<{ status: AuthStatus }> =
    await axiosInstance.post('/auth/login_otp', {
      phoneNumber,
      verificationCode: otp,
    });
  return data.status;
}

export { login, loginOtp };
