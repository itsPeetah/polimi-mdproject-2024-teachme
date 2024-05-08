import { HeadingL } from "@/components/headings";
import Link from "next/link";
import React, { useState } from "react";
import { useForm } from "react-hook-form";

export default function LoginPage() {
  const [activeTab, setActiveTab] = useState("teacher");
  const { register, handleSubmit } = useForm();

  const login = (data) => {
    fetch("http://localhost:3000/login", {
      method: "POST",
      body: JSON.stringify({ email: data.email, password: data.password }),
    })
      .then((response) => response.json())
      .then((data) => console.log(data));
  };

  return (
    // MAIN
    <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center text-white">
      {/* Container */}
      <div className="bg-slate-800 bg-opacity-90 backdrop-blur-md p-8 rounded-lg shadow-md w-full max-w-md relative">
        <HeadingL text={"Login"} />
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
