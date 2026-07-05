import { createRemoteJWKSet, jwtVerify } from 'jose';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

import { LOGIN_ROUTE } from '@/constants/routes';

const JWKS = createRemoteJWKSet(
  new URL(`${process.env.MIDDLEWARE_BACKEND_URL}/jwks.json`),
);

// These codes just mean that validation failed in some way, and that's not log
// worthy.
const EXPECTED_AUTH_FAILURES = new Set([
  'ERR_JWT_EXPIRED',
  'ERR_JWT_CLAIM_VALIDATION_FAILED',
  'ERR_JWS_SIGNATURE_VERIFICATION_FAILED',
  'ERR_JWS_INVALID',
  'ERR_JWT_INVALID',
  'ERR_JWKS_NO_MATCHING_KEY',
]);

export async function proxy(req: NextRequest) {
  const token = req.cookies.get('access_token')?.value;
  if (token) {
    try {
      const { payload } = await jwtVerify(token, JWKS);
      const headers = new Headers(req.headers);
      headers.set('x-user-id', String(payload.user_id ?? ''));
      return NextResponse.next({ request: { headers } });
    } catch (error) {
      // Only log the error if it's not an authentication failure
      const code = (error as { code?: string })?.code;
      if (!code || !EXPECTED_AUTH_FAILURES.has(code)) {
        console.error('proxy: could not verify access token', error);
      }
    }
  }
  const url = req.nextUrl.clone();
  const loginUrl = new URL(LOGIN_ROUTE, req.url);
  loginUrl.searchParams.set('next', url.pathname + url.search);
  return NextResponse.redirect(loginUrl);
}

// Apply middleware to all pages except /login, /, and static files
export const config = {
  matcher: ['/test/:path*'],
};
