import "@/styles/globals.css";
import type { AppProps } from "next/app";
import "regenerator-runtime/runtime"; // for react-speech recognition
export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
