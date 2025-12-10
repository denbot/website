export type AuthStatus =
  | 'initial'
  | 'created'
  | 'approved'
  | 'failed'
  | 'expired'
  | 'error'
  | 'too_many_attempts';
