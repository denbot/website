import { AxiosError } from 'axios';
import useSWR from 'swr';

import { SWRHookReturn } from '@/models/swr-hook-return.model';
import { getCurrentUser } from '@/services/user';

function useCurrentUser(): SWRHookReturn<string> {
  const { data, error, isLoading } = useSWR<string, AxiosError>('', () =>
    getCurrentUser(),
  );

  return {
    data: data,
    isLoading,
    error,
  };
}

export { useCurrentUser };
