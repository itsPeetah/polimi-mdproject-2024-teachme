import Link from "next/link";
import { useRouter } from "next/router";
import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import useSWR from "swr";
import { getCookie } from "cookies-next";
import { HeadingL } from "@/components/Headings";
import Head from "next/head";
import { BACKEND_URL_BASE } from "@/lib/constants";

export default function CreatePage() {
  const router = useRouter();
  const fetcher = (...args) => fetch(...args).then((res) => res.json());
  const { register, handleSubmit } = useForm();
  const [students, setStudents] = useState([]);

  //  Fetch Current Students
  const url3 = `${BACKEND_URL_BASE}/get-friends/${getCookie("email")}`;
  const { data, error } = useSWR(url3, fetcher);
  useEffect(() => {
    if (data) {
      setStudents(data);
    } else if (error) {
      setIsError(true);
      console.log(error);
    }
  }, [data, error]);

  // Create Conversation Function
  const create = async (data) => {
    const url = `${BACKEND_URL_BASE}/create-conversation`;
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_level: data.userLevel,
          difficulty: data.difficulty,
          topic: data.topic,
          teacher_email: getCookie('email'),
          student_email: data.studentEmail,
          time_limit: data.duration,
        }),
      });
      if (response.ok) {
        alert("Conversation Created");
        router.push("/teacher");
      } else {
        alert("Error");
      }
    } catch (error) {
      console.log(error);
    }
  };
  return (
    // MAIN
    <div className="h-screen bg-art flex flex-col items-center justify-center">
      <Head>
        <title>TeachMe | Create Conversation</title>
      </Head>
      {/* Container */}
      <div
        className="
                    flex flex-col justify-center items-center
                    bg-slate-900/40 backdrop-blur-md shadow-md p-10 rounded-lg 
                    w-11/12 lg:w-8/12 h-5/6
                "
      >
        <HeadingL text={"Creating New Content"} />
        {/* FORM */}
        <form
          className={`w-1/2 mb-4 flex flex-col gap-6`}
          onSubmit={handleSubmit(create)}
        >
          {/* User Level */}
          <select
            className="form-input"
            id="userLevel"
            {...register("userLevel", { required: true })}
          >
            <option value={""}>Select User Level</option>
            <option value={"beginner"}>Beginner</option>
            <option value={"intermediate"}>Intermediate</option>
            <option value={"advanced"}>Advanced</option>
          </select>
          {/* difficulty */}
          <select
            className="form-input"
            id="difficulty"
            {...register("difficulty", { required: true })}
          >
            <option value={""}>Select Difficulty</option>
            <option value={"easy"}>Easy</option>
            <option value={"medium"}>Medium</option>
            <option value={"challenging"}>Challenging</option>
          </select>
          {/* Student Email */}
          <select
            className="form-input"
            type="email"
            id="topic"
            placeholder="Student Email"
            {...register("studentEmail", { required: true })}
          >
            <option value={""}>Select Student</option>
            {students.map((student, index) => (
              <option key={index} value={student}>
                {student}
              </option>
            ))}
          </select>
          {/* Duration */}
          <input
            className="form-input"
            id="duration"
            type="number"
            min={1}
            placeholder="Duration in Minutes"
            {...register("duration")}
          />
          {/* Topic */}
          <input
            className="form-input"
            type="text"
            id="topic"
            placeholder="Topic"
            {...register("topic")}
          />
          {/* SUBMIT BUTTON */}
          <button type="submit" className="submit-btn mt-4">
            Create
          </button>
          <Link href="/teacher" className="cancle-btn">
            Cancle
          </Link>
        </form>
      </div>
    </div>
  );
}
