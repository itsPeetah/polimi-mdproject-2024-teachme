import Link from "next/link";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
// APIs
import useSWR from "swr";
import { getCookie } from "cookies-next";
import "animate.css";
import { FiPlusSquare, FiUserPlus } from "react-icons/fi";
import { DNA } from "react-loader-spinner";
// Components
import { SideMenuBtn } from "@/components/SideMenuBtn";
import { SideMenu } from "@/components/SideMenu";
import Head from "next/head";
import { BACKEND_URL_BASE } from "@/lib/constants";

export default function TeacherPage() {
  // --- States ---
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [name, setName] = useState("");
  const [students, setStudents] = useState([]);
  const [feedbacks, setFeedbacks] = useState([]);
  const [showMenu, setShowMenu] = useState(false);

  // --- Constants ---
  const router = useRouter();
  const fetcher = (...args) => fetch(...args).then((res) => res.json());

  // --- Functions ---
  // Side-Menu Handler
  const toggleMenu = () => {
    setShowMenu(!showMenu);
  };

  // --- REST APIs ---
  // Fetch user info
  const url = `${BACKEND_URL_BASE}/get-username/${getCookie("email")}`;
  const { data: infoData, error: infoError } = useSWR(url, fetcher);
  useEffect(() => {
    if (infoData) {
      setName(infoData["username"]);
      setStudents(infoData["friends"]);
    } else if (infoError) {
      setIsError(true);
    }
  }, [infoData, infoError]);

  // Fetch List of user conversations
  const url2 = `${BACKEND_URL_BASE}/list-user-conversations/${getCookie(
    "email"
  )}`;
  const { data, error } = useSWR(url2, fetcher);
  useEffect(() => {
    if (data) {
      setIsLoading(false);
      for (let element of data) {
        if (element["is_ended"]) {
          setFeedbacks((feedbacks) => [...feedbacks, element]);
        }
      }
    } else if (error) {
      setIsError(true);
    }
  }, [data, error]);

  // RENDER
  return (
    <div className="min-h-screen w-full bg-art flex flex-row">
      <Head>
        <title>TeachMe | Teacher Dashboard</title>
      </Head>
      {/* Toggle Side-Menu Button*/}
      <SideMenuBtn showMenu={showMenu} toggleMenu={toggleMenu} />
      {/* Side-Menu */}
      <SideMenu showMenu={showMenu} name={name} />
      {/* Dashboard */}
      <div className="flex-1 flex flex-col items-center overflow-y-scroll py-10">
        <h1 className="header1">Teacher Dashboard</h1>
        {/* Loading */}
        {isLoading && <DNA width={150} height={150} />}
        {/* Error */}
        {isError && (
          <h1 className="text-rose-800 font-bold text-2xl">Server Error!</h1>
        )}
        {/* Conversations Section */}
        <Conversations data={data} />
        {/* Feedbacks Section */}
        <Feedbacks data={feedbacks} />
        {/* Students Section */}
        <Students students={students} />
      </div>
    </div>
  );
}

// --- COMPONENTS ---

function Conversations(props) {
  return (
    <section className="my-10 w-10/12">
      <h2 className="header2">Conversations</h2>
      {/* Conversations */}
      <ul className="flex flex-row flex-wrap items-center justify-center gap-5">
        {/* Create Conversation Button */}
        <li className="conversation-card">
          <Link
            href={"/teacher/create"}
            className="flex h-full w-full items-center justify-center rounded-2xl bg-slate-900/40 text-center backdrop-blur"
          >
            <FiPlusSquare size={44} />
          </Link>
        </li>
        {/* List of Conversations */}
        {props.data &&
          props.data.map((item, index) => (
            <li key={index}>
              <Link
                href={"/student/conversation/" + item["_id"]}
                className="conversation-card"
              >
                <h1 className="font-display text-lg">Topic: {item["topic"]}</h1>
                <h2 className="font-display text-md">
                  Difficuly: {item["difficulty"]}
                </h2>
                <h2 className="font-display text-md">
                  Level: {item["user_level"]}
                </h2>
                <h2 className="font-display text-md">
                  student: {item["student_email"]}
                </h2>
              </Link>
            </li>
          ))}
      </ul>
    </section>
  );
}

// Feedbacks Section
function Feedbacks(props) {
  const { data } = props;
  return (
    <section className="my-10 w-10/12 flex flex-col justify-start items-center">
      <h2 className="header2">Feedbacks</h2>
      <ul className="flex flex-row flex-wrap items-center justify-center gap-5">
        {data &&
          data.map((item, index) => (
            <li key={index}>
              <Link
                href={"/teacher/feedback/" + item["_id"]}
                className="feedback-card"
              >
                <h1 className="font-display text-lg">Topic: {item["topic"]}</h1>
                <h2 className="font-display text-md">
                  Difficuly: {item["difficulty"]}
                </h2>
                <h2 className="font-display text-md">
                  Level: {item["user_level"]}
                </h2>
                <h2 className="font-display text-md">
                  student: {item["student_email"]}
                </h2>
              </Link>
            </li>
          ))}
      </ul>
    </section>
  );
}

function Students(props) {
  return (
    <section className="my-10">
      <h2 className="header2">Students</h2>
      <ul className="flex flex-row flex-wrap items-center justify-center gap-5">
        {/* Add Student Button */}
        <li className="student-card bg-sky-900">
          <Link
            href={"/teacher/manage-students"}
            className="h-full w-full flex justify-center items-center"
          >
            <FiUserPlus size={36} />
          </Link>
        </li>
        {/* List of Students */}
        {props.students.map((student, index) => (
          <li key={index} className="student-card font-display text-md">
            {student}
          </li>
        ))}
      </ul>
    </section>
  );
}
