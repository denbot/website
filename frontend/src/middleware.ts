import { NextURL } from 'next/dist/server/web/next-url';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(req: NextRequest) {
  const url: NextURL = req.nextUrl.clone();

  // TODO: Actually verify not just check existence
  const isLoggedIn = req.cookies.get('authToken');

  if (!isLoggedIn) {
    const loginUrl = new URL('/login', req.url);
    loginUrl.searchParams.set('next', url.pathname + url.search);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

// Apply middleware to all pages except /login, /, and static files
export const config = {
  matcher: ['/((?!login$|$|_next/).*)'],
};
