export type AuthStatus =
  | 'initial'
  | 'pending'
  | 'approved'
  | 'canceled'
  | 'max_attempts_reached'
  | 'deleted'
  | 'failed'
  | 'expired';

export interface AuthFlowResponse {
  error: boolean;
  status: AuthStatus;
}
