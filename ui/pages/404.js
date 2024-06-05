import Link from 'next/link'

export default function NotFound() {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-slate-900">
            <h1 className="text-4xl font-bold text-slate-200 mb-4">404 - Page Not Found</h1>
            <p className="text-lg text-slate-400 mb-8">Sorry, the page you are looking for does not exist.</p>
            <Link href="/" className="text-blue-300 hover:text-blue-500">Go back to Home</Link>
        </div>
    )
}