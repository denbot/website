import { SWRHookReturn } from '@/models/swr-hook-return.model';
import { getUser } from '@/services/user';
import { AxiosError } from 'axios';
import useSWR from 'swr';

function useUser(id: string): SWRHookReturn<string> {
  const { data, error, isLoading } = useSWR<string, AxiosError>('', () =>
    getUser(id),
  );

  return {
    data: data,
    isLoading,
    error,
  };
}

export { useUser };
