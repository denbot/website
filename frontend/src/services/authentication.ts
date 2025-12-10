import type { AxiosResponse } from 'axios';
import toast from 'react-hot-toast';

import { AuthStatus } from '@/models/auth-flow-response.model';

import { axiosInstance } from './axios';

async function login(phoneNumber: string): Promise<AuthStatus> {
  try {
    const { data }: AxiosResponse<{ status: AuthStatus }> =
      await axiosInstance.post('/auth/login', { phoneNumber });
    if (!!data.status) {
      return data.status;
    }
    return 'error';
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
    if (!!data.status) {
      return data.status;
    }
    return 'error';
  } catch {
    return 'error';
  }
}

export { login, loginOtp };
