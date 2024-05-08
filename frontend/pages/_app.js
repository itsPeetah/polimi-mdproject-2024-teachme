import {regeneratorRuntime} from "regenerator-runtime";
import '@/public/styles/globals.css'
import { Inter, Arima } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })
const arima = Arima({
  subsets: ['latin'],
  variable: '--font-arima',
})
export default function App({ Component, pageProps }) {
  return (
    <main className={`${inter.className} ${arima.variable} bg-slate-900 text-white`}>
      <Component {...pageProps} />
    </main>
  )
}