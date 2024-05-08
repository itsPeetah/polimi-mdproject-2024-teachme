import { HeadingL } from "@/components/headings";
import Link from "next/link";
import React, { useState } from "react";

export default function LoginPage() {
  const [activeTab, setActiveTab] = useState("teacher");

  const { register, handleSubmit } = useForm();

  const signup = (data) => {
    fetch("http://localhost:3000/register", {
      method: "POST",
      body: JSON.stringify({
        name: data.name,
        email: data.email,
        password: data.password,
      }),
    })
      .then((response) => response.json())
      .then((data) => console.log(data));
  };

  return (
    // MAIN
    <div className="flex flex-col items-center justify-center min-h-screen text-white bg-slate-900">
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
        {/* FORM */}
        <form className="mb-4" onSubmit={handleSubmit(signup)}>
          {/* Name INPUT */}
          <div className="mb-4">
            <label
              htmlFor="name"
              className="block mb-2 text-sm font-medium text-gray-300"
            >
              Name
            </label>
            <input
              type="text"
              id="name"
              {...register("name", { required: true })}
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
