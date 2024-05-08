import Link from 'next/link';
import { useEffect, useRef } from 'react';

export default function Home() {
  const ref = useRef(null);
  useEffect(() => {
    import("@lottiefiles/lottie-player");
  });
  return (
    <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center text-white px-4">
      <h1 className="text-4xl lg:text-5xl font-display font-bold mb-8 text-center">
        Learn English as a Second Language
      </h1>
      <p className="text-lg lg:text-xl mb-8 max-w-lg text-center">
        Welcome to our platform where you can improve your English skills. Whether you&apos;re a beginner or an advanced learner, we&apos;ve got you covered!
      </p>
      <div className='mb-10 lg:w-1/3'>
        <lottie-player
          src='/lottie/intro.json'
          ref={ref}
          loop autoplay
        />
      </div>
      <Link
        href='/auth/login'
        className="bg-blue-700 hover:bg-blue-600 text-white font-bold py-4 px-8 rounded-full shadow-lg transition duration-300 ease-in-out transform hover:scale-105"
      >
        Start Learning
      </Link>
      {/* TEMP LINKS */}
      <Link
        href='/student'
        className="m-8 text-white font-bold"
      >
        STUDENT
      </Link>
      <Link
        href='/teacher'
        className="font-bold"
      >
        TEACHER
      </Link>
    </div>
  )
}
