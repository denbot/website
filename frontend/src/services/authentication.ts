import { AxiosResponse } from 'axios';
import { axiosInstance } from './axios';

async function login(phoneNumber: string): Promise<string> {
  const loginResult: AxiosResponse<string> = await axiosInstance.post(
    '/authentication/login',
    phoneNumber,
  );
  return loginResult.data;
}

async function loginOtp(otp: string): Promise<string> {
  const loginOtpResult: AxiosResponse<string> = await axiosInstance.post(
    '/authentication/login_otp',
    otp,
  );
  return loginOtpResult.data;
}

export { login, loginOtp };
