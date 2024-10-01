import { NextResponse } from 'next/server'

export function middleware(request) {
    const token = request.cookies.get('auth-token')?.value
    const { pathname } = request.nextUrl;
    
    const loginURL = new URL('/', request.url);
    const logadoURL = new URL('/logado', request.url)

    const pathPublico = pathname === '/' || pathname === '/registrar'

    if (!token && !pathPublico) {
        return NextResponse.redirect(loginURL)
    }

    if (token && pathPublico) {
        return NextResponse.redirect(logadoURL)
    }

    return NextResponse.next()
}

export const config = {
    matcher: ['/', '/logado/:path*', '/registrar']
};

