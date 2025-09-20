'use client';

import { axiosInstance } from '@/services/axios';
import { ReactElement } from 'react';

export function LoginButton(): ReactElement {
  const login = () => {
    axiosInstance.get('/').then(console.log);
  };

  return <button onClick={login}>click here</button>;
}

export default LoginButton;
