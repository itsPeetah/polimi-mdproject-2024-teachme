import React from "react";

export default function register() {
  return (
    <div>
      register
      <form
        id="signup"
        action="http://localhost:5000/register"
        method="POST"
        className="flex flex-col gap-4 p-4 | bg-gray-400"
      >
        <input name="email" placeholder="email"></input>
        <input name="username" placeholder="username"></input>
        <input name="password" placeholder="password"></input>
        <select name="role" form="signup">
          <option value={"student"}>Student</option>
          <option value={"teacher"}>Teacher</option>
        </select>
        <button type="submit">Submit</button>
      </form>
      login
      <form
        id="signup"
        action="http://localhost:5000/login"
        method="POST"
        className="flex flex-col gap-4 p-4 | bg-gray-400"
      >
        <input name="email" placeholder="email"></input>
        {/* <input name="username" placeholder="username"></input> */}
        <input name="password" placeholder="password"></input>
        {/* <select name="role" form="signup">
          <option value={"student"}>Student</option>
          <option value={"teacher"}>Teacher</option>
        </select> */}
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}
