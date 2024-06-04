import { NextResponse } from 'next/server'

// This function can be marked `async` if using `await` inside
export function middleware(request) {
    let id = request.cookies.get('id')
    let email = request.cookies.get('email')
    let role = request.cookies.get('role')
    if (
        request.nextUrl.pathname.startsWith('/teacher') ||
        request.nextUrl.pathname.startsWith('/student')
    ) {
        if (!id || !email || !role) {
            return NextResponse.redirect(new URL('/auth/login', request.url))
        }
        else if (request.nextUrl.pathname.startsWith('/teacher') && role.value !== 'teacher') {
            return NextResponse.redirect(new URL('/student', request.url))
        }
        else if (request.nextUrl.pathname.startsWith('/student') && role.value !== 'student') {
            return NextResponse.redirect(new URL('/teacher', request.url))
        }
    }
    else if (request.nextUrl.pathname.startsWith('/auth') && id && email && role) {
        if (role.value === 'teacher') {
            return NextResponse.redirect(new URL('/teacher', request.url))
        } else {
            return NextResponse.redirect(new URL('/student', request.url))
        }
    }
    else {
        return NextResponse.next()
    }
}
// See "Matching Paths" below to learn more
export const config = {
    matcher: ['/teacher/:path*', '/student/:path*', '/auth/:path*']
}