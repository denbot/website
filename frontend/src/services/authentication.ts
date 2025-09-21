import { AxiosResponse } from 'axios';
import { axiosInstance } from './axios';
import {
  AuthFlowResponse,
  AuthStatus,
} from '@/models/auth-flow-response.model';

async function login(phoneNumber: string): Promise<AuthFlowResponse> {
  const { data, status }: AxiosResponse<{ status: AuthStatus }> =
    await axiosInstance.post('/auth/login', { phoneNumber });
  return { error: status != 200, status: data.status };
}

async function loginOtp(
  phoneNumber: string,
  otp: string,
): Promise<AuthFlowResponse> {
  const { data, status }: AxiosResponse<{ status: AuthStatus }> =
    await axiosInstance.post('/auth/login_otp', {
      phoneNumber,
      verificationCode: otp,
    });
  return { error: status != 200, status: data.status };
}

export { login, loginOtp };
