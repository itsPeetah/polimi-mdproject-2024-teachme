import { HeadingL } from "@/components/Headings";
import Link from "next/link";
import { useRouter } from "next/router";
import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { setCookie } from "cookies-next";
import Head from "next/head";
import { BACKEND_URL_BASE } from "@/lib/constants";
export default function SignupPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState("teacher");
  const { register, handleSubmit } = useForm();
  const [error, setError] = useState(false);
  const url = `${BACKEND_URL_BASE}/register`;
  // Signup function
  const signup = async (data) => {
    const formData = new FormData();
    // Append data to the FormData object
    formData.append("email", data.email);
    formData.append("username", data.username);
    formData.append("password", data.password);
    formData.append("role", activeTab);
    // Send POST request
    try {
      let res = await fetch(url, {
        method: "POST",
        body: formData, // Pass FormData object as body
      });
      if (res.ok) {
        const resData = await res.json();
        setCookie("id", resData.uid);
        setCookie("role", activeTab);
        setCookie("email", data.email);
        if (activeTab === "teacher") {
          router.push("/teacher");
        } else if (activeTab === "student") {
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
    <div className="flex flex-col items-center justify-center min-h-screen text-white bg-slate-900">
      <Head>
        <title>TeachMe | Sign-Up</title>
      </Head>
      {/* Container */}
      <div className="relative w-full max-w-md p-8 rounded-lg shadow-md bg-slate-800 bg-opacity-90 backdrop-blur-md">
        <HeadingL text={"Sign-Up"} />
        {/* TABS */}
        <div className="flex mb-10">
          <button
            className={`
                            flex-1 py-2 px-4 text-center 
                            ${
                              activeTab === "teacher"
                                ? "bg-blue-600 text-white"
                                : "bg-gray-700 text-gray-300 hover:bg-gray-600 hover:text-white"
                            } 
                            rounded-tl-lg rounded-bl-lg transition duration-300 ease-in-out`}
            onClick={() => setActiveTab("teacher")}
          >
            Teacher
          </button>
          <button
            className={`
                            flex-1 py-2 px-4 text-center 
                            ${
                              activeTab === "student"
                                ? "bg-blue-600 text-white"
                                : "bg-gray-700 text-gray-300 hover:bg-gray-600 hover:text-white"
                            } 
                            rounded-tr-lg rounded-br-lg transition duration-300 ease-in-out`}
            onClick={() => setActiveTab("student")}
          >
            Student
          </button>
        </div>
        {/* ERROR MESSAGE */}
        <h2
          className={`${
            error ? "block" : "hidden"
          } text-center text-md text-red-400 mb-4`}
        >
          Server error! Please try again later.
        </h2>
        {/* FORM */}
        <form className="mb-4" onSubmit={handleSubmit(signup)}>
          {/* Name INPUT */}
          <div className="mb-4">
            <label
              htmlFor="username"
              className="block mb-2 text-sm font-medium text-gray-300"
            >
              Name
            </label>
            <input
              type="text"
              id="username"
              {...register("username", { required: true })}
              className="w-full px-3 py-2 text-gray-300 transition duration-300 ease-in-out bg-gray-700 rounded-md shadow-lg focus:outline-none focus:ring focus:border-blue-300"
            />
          </div>
          {/* EMAIL INPUT */}
          <div className="mb-4">
            <label
              htmlFor="email"
              className="block mb-2 text-sm font-medium text-gray-300"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              {...register("email", { required: true })}
              className="w-full px-3 py-2 text-gray-300 transition duration-300 ease-in-out bg-gray-700 rounded-md shadow-lg focus:outline-none focus:ring focus:border-blue-300"
            />
          </div>
          {/* PASSWORD INPUT */}
          <div className="mb-8">
            <label
              htmlFor="password"
              className="block mb-2 text-sm font-medium text-gray-300"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              {...register("password", { required: true })}
              className="w-full px-3 py-2 text-gray-300 transition duration-300 ease-in-out bg-gray-700 rounded-md shadow-lg focus:outline-none focus:ring focus:border-blue-300"
            />
          </div>
          {/* SUBMIT BUTTON */}
          <button
            type="submit"
            className="w-full px-4 py-2 mb-4 font-bold text-white transition duration-300 ease-in-out bg-blue-600 rounded-md hover:bg-blue-700"
          >
            Sign-up
          </button>
        </form>

        <Link
          href="/auth/login"
          className="text-sm text-blue-100 transition duration-300 ease-in-out hover:text-blue-200"
        >
          Already have an account? Login
        </Link>
      </div>
    </div>
  );
}
