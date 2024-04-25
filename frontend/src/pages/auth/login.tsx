import getEndpoint from "@/lib/api/getEndpoint";
import React from "react";

const FORM_ACTION = getEndpoint("login");

export default function Login() {
  console.log(FORM_ACTION);
  return (
    <main className="w-screen h-screen | flex flex-col items-center justify-center gap-10 | bg-slate-100">
      <h1 className="text-4xl">Welcome back, please log in</h1>
      <form
        id="form__signin"
        method="POST"
        action={FORM_ACTION}
        className="flex flex-col gap-5 | py-5 px-20 | bg-gradient-to-b from-slate-200 to-slate-300 rounded-xl shadow-lg"
      >
        <label htmlFor="form__email">Email</label>
        <input
          className="shadow-xl"
          id="form__email"
          name="email"
          type="email"
          placeholder="Email..."
        />
        <label htmlFor="form__password">Password</label>
        <input
          className="shadow-xl"
          id="form__password"
          name="password"
          type="password"
          placeholder="Password..."
        />
        <button
          type="submit"
          className="p-2 | rounded-md bg-gradient-to-b from-sky-400 to-sky-500 hover:bg-gradient-to-t"
        >
          Log in
        </button>
      </form>
    </main>
  );
}
