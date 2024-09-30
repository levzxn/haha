import { NextResponse } from 'next/server'

export function middleware(request) {
    const token = request.cookies.get('auth-token')?.value
    const loginURL = new URL('/', request.url)
    const logadoURL = new URL('/logado', request.url)
    const registroURL = new URL('/registrar', request.url)
    if (!token){
        if(request.nextUrl.pathname === '/registrar' || request.nextUrl.pathname === '/'){
            return NextResponse.next()
        }
        return NextResponse.redirect(loginURL)
    }
    if (request.nextUrl.pathname === '/'){
        return NextResponse.redirect(logadoURL)
    }
    if (request.nextUrl.pathname === '/registrar'){
        return NextResponse.redirect(logadoURL)
    }
}

export const config = {
    matcher: ['/', '/logado', '/registrar']
}
