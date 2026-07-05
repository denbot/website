// Shared route constants so the proxy and the login flow agree on these paths.

// Where an authenticated user lands when there's no explicit `next` target.
export const DEFAULT_LANDING_PAGE = '/';

// The login page: proxy redirects here on auth failure.
export const LOGIN_ROUTE = '/login';
