import { NextURL } from 'next/dist/server/web/next-url';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(req: NextRequest) {
  const url: NextURL = req.nextUrl.clone();

  const cookieHeader: string = req.headers.get('cookie') ?? '';

  // TODO: this seems a bit off, rethink/rework
  try {
    const fetchResult: Response = await fetch(
      `http://nginx/api/auth/validate_user`,
      {
        headers: {
          Host: req.nextUrl.host,
          cookie: cookieHeader,
        },
      },
    );
    const isLoggedIn: boolean = fetchResult.status == 200;

    if (!isLoggedIn) {
      const loginUrl = new URL('/login', req.url);
      loginUrl.searchParams.set('next', url.pathname + url.search);
      return NextResponse.redirect(loginUrl);
    }

    return NextResponse.next();
  } catch {
    // server problem -> assume not logged in
    // TODO -> send to server error page?
    const loginUrl = new URL('/login', req.url);
    loginUrl.searchParams.set('next', url.pathname + url.search);
    return NextResponse.redirect(loginUrl);
  }
}

// Apply middleware to all pages except /login, /, and static files
export const config = {
  matcher: ['/((?!login$|$|_next/|images).*)'],
};
