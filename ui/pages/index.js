import Head from 'next/head';
import Link from 'next/link';
import { useEffect, useRef } from 'react';

export default function Home() {
  const ref = useRef(null);
  useEffect(() => {
    import("@lottiefiles/lottie-player");
  });
  return (
    <div className="w-screen min-h-screen bg-slate-900 flex flex-col items-center text-white p-10">
      <Head>
        <title>TeachMe</title>
      </Head>
      <h1 className="text-4xl lg:text-5xl font-display font-bold mb-8 text-center">
        TeachMe
      </h1>
      <p className="text-lg lg:text-xl mb-8 max-w-lg text-center">
        Welcome to our platform where you can improve your speaking English skills. Whether you&apos;re a beginner or an advanced learner, we&apos;ve got you covered!
      </p>
      <div className='mb-10 w-[300px] sm:w-[500px]'>
        <lottie-player
          src='/lottie/intro.json'
          ref={ref}
          loop autoplay
        />
      </div>
      <Link
        href='/auth/login'
        className="bg-blue-700 hover:bg-blue-600 text-white font-bold py-5 px-20 rounded-full shadow-lg transition duration-300 ease-in-out transform hover:scale-105 my-auto"
      >
        Start Learning
      </Link>
    </div>
  )
}
