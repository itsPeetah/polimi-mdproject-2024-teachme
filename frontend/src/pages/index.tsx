import Link from "next/link";

export default function Home() {
  return (
    <main className={`flex min-h-screen flex-col items-center p-24`}>
      <h3 className="my-5 font-bold">main</h3>
      <Link href="/student">Student App</Link>
      <Link href="/teacher">Teacher App</Link>
      <h3 className="my-5 font-bold">test</h3>
      <Link href="/test/chat">Test Chat</Link>
    </main>
  );
}
