import Link from "next/link";
import { useRouter } from "next/router";
import { useState } from "react";
// APIs
import { useForm } from "react-hook-form";
import { setCookie } from "cookies-next";
// Components
import { HeadingL } from "@/components/Headings";
import Head from "next/head";
import { BACKEND_URL_BASE } from "@/lib/constants";

export default function LoginPage() {
  const router = useRouter();
  const { register, handleSubmit } = useForm();
  const [error, setError] = useState(false);
  const url = `${BACKEND_URL_BASE}/login`;
  // Login function
  const login = async (data) => {
    // Create a FormData object
    const formData = new FormData();
    // Append email and password to the FormData object
    formData.append("email", data.email);
    formData.append("password", data.password);
    try {
      let res = await fetch(url, {
        method: "POST",
        body: formData, // Pass FormData object as body
      });
      if (res.ok) {
        let resData = await res.json();
        setCookie("id", resData.uid);
        setCookie("role", resData.role);
        setCookie("email", data.email);
        if (resData.role === "teacher") {
          router.push("/teacher");
        } else if (resData.role === "student") {
          router.push("/student");
        }
      } else {
        setError(true);
      }
    } catch (error) {
      setError(true);
      console.error(error);
    }
  };
  return (
    // MAIN
    <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center text-white">
      <Head>
        <title>TeachMe | Login</title>
      </Head>
      {/* Container */}
      <div className="bg-slate-800 bg-opacity-90 backdrop-blur-md p-8 rounded-lg shadow-md w-full max-w-md relative">
        <HeadingL text={"Login"} />
        {/* ERROR MESSAGE */}
        <h2
          className={`${
            error ? "block" : "hidden"
          } text-center text-md text-red-400 mb-4`}
        >
          Incorrect email or password!
        </h2>
        {/* FORM */}
        <form className="mb-4" onSubmit={handleSubmit(login)}>
          {/* EMAIL INPUT */}
          <div className="mb-4">
            <label
              htmlFor="email"
              className="block text-sm font-medium mb-2 text-gray-300"
            >
              Email
            </label>
            <input
              type="email"
              {...register("email", { required: true })}
              id="email"
              className="w-full px-3 py-2 shadow-lg rounded-md bg-gray-700 text-gray-300 focus:outline-none focus:ring focus:border-blue-300 transition duration-300 ease-in-out"
            />
          </div>
          {/* PASSWORD INPUT */}
          <div className="mb-8">
            <label
              htmlFor="password"
              className="block text-sm font-medium mb-2 text-gray-300"
            >
              Password
            </label>
            <input
              type="password"
              {...register("password", { required: true })}
              id="password"
              className="w-full px-3 py-2 shadow-lg rounded-md bg-gray-700 text-gray-300 focus:outline-none focus:ring focus:border-blue-300 transition duration-300 ease-in-out"
            />
          </div>
          {/* SUBMIT BUTTON */}
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 mb-4 rounded-md transition duration-300 ease-in-out"
          >
            Log in
          </button>
        </form>

        <Link
          href="/auth/signup"
          className="text-blue-100 hover:text-blue-200 transition duration-300 ease-in-out text-sm"
        >
          Don&apos;t have an account? Sign-Up
        </Link>
      </div>
    </div>
  );
}
