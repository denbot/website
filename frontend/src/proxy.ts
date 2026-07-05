import { createRemoteJWKSet, jwtVerify } from 'jose';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

import { LOGIN_ROUTE } from '@/constants/routes';

const JWKS = createRemoteJWKSet(
  new URL(`${process.env.MIDDLEWARE_BACKEND_URL}/jwks.json`),
);

export async function proxy(req: NextRequest) {
  const token = req.cookies.get('access_token')?.value;
  if (token) {
    try {
      const { payload } = await jwtVerify(token, JWKS);
      const headers = new Headers(req.headers);
      headers.set('x-user-id', String(payload.user_id ?? ''));
      return NextResponse.next({ request: { headers } });
    } catch (error) {
      console.log('error', error);
      // Auth failed, fall through to login
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
