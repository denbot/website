import { AxiosResponse } from 'axios';
import { axiosInstance } from './axios';

async function login(phoneNumber: string): Promise<boolean> {
  const loginResult: AxiosResponse<{ success: boolean }> =
    await axiosInstance.post('/auth/login', { phoneNumber });
  return loginResult.data.success;
}

async function loginOtp(phoneNumber: string, otp: string): Promise<boolean> {
  const loginOtpResult: AxiosResponse<{ success: boolean }> =
    await axiosInstance.post('/auth/login_otp', {
      phoneNumber,
      verificationCode: otp,
    });
  return loginOtpResult.data.success;
}

export { login, loginOtp };
