import ClientSideAppUI from "@/lib/app";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <main
      className={`flex min-h-screen flex-col gap-4 p-24 ${inter.className}`}
    >
      <ClientSideAppUI />
    </main>
  );
}
