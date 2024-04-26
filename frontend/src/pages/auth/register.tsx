import getEndpoint from "@/lib/api/getEndpoint";
import React from "react";

const FORM_ACTION = getEndpoint("register");

export default function Register() {
  return (
    <main className="w-screen h-screen | flex flex-col items-center justify-center gap-10 | bg-slate-100">
      <h1 className="text-4xl">Register</h1>
      <form
        id="form__signup"
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
        <label htmlFor="form__username">Username</label>
        <input
          className="shadow-xl"
          id="form__username"
          name="username"
          type="text"
          placeholder="Username..."
        />
        <label htmlFor="form__password">Password</label>
        <input
          className="shadow-xl"
          id="form__password"
          name="password"
          type="password"
          placeholder="Password..."
        />
        <label htmlFor="form__role">What&apos;s your role?</label>
        <select
          form="form__signup"
          id="form__role"
          name="role"
          className="shadow-xl"
        >
          <option value="student">I&apos;m a Student</option>
          <option value="teacher">I&apos;m a Teacher</option>
        </select>
        <button
          type="submit"
          className="p-2 | rounded-md bg-gradient-to-b from-sky-400 to-sky-500 hover:bg-gradient-to-t"
        >
          Register
        </button>
      </form>
    </main>
  );
}
