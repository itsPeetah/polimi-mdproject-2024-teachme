import Link from "next/link";
import { useRouter } from "next/router";
import { useState, useEffect } from "react";
// APIs
import "animate.css";
import { getCookie } from "cookies-next";
import useSWR from "swr";
import { DNA } from "react-loader-spinner";
// Components
import { SideMenu } from "@/components/SideMenu";
import { SideMenuBtn } from "@/components/SideMenuBtn";
import Head from "next/head";

export default function StudentPage() {
  // Constants
  const router = useRouter();
  const fetcher = (...args) => fetch(...args).then((res) => res.json());

  // States
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [name, setName] = useState("");
  const [feedbacks, setFeedbacks] = useState([]);

  // Fetch user info
  const url = "http://127.0.0.1:5000/get-username/" + getCookie("email");
  const { data: infoData, error: infoError } = useSWR(url, fetcher);
  useEffect(() => {
    if (infoData) {
      setName(infoData["username"]);
    } else if (infoError) {
      setIsError(true);
    }
  }, [infoData, infoError]);

  // Fetch List of user conversations
  const url2 =
    "http://127.0.0.1:5000/list-user-conversations/" + getCookie("email");
  const { data, error } = useSWR(url2, fetcher);
  useEffect(() => {
    if (data) {
      setIsLoading(false);
      const conversationFeedbacks = [];
      for (let element of data) {
        if (element["is_ended"]) conversationFeedbacks.push(element);
      }
      setFeedbacks(conversationFeedbacks);
    } else if (error) {
      setIsError(true);
    }
  }, [data, error]);

  // Side-Menu Handler
  const [showMenu, setShowMenu] = useState(false);
  const toggleMenu = () => {
    setShowMenu(!showMenu);
  };

  // Render
  return (
    <div className="flex flex-row w-full min-h-screen bg-art">
      <Head>
        <title>TeachMe | Student Dashboard</title>
      </Head>
      {/* Toggle Side-Menu Button*/}
      <SideMenuBtn showMenu={showMenu} toggleMenu={toggleMenu} />
      {/* Side-Menu */}
      <SideMenu name={name} showMenu={showMenu} />
      {/* Dashboard */}
      <div className="flex-1 flex flex-col items-center px-x py-10 overflow-y-scroll">
        {/* Heading */}
        <h1 className="header1">Student Dashboard</h1>
        {/* Loading */}
        {isLoading && <DNA width={150} height={150} />}
        {/* Error */}
        {isError && (
          <h1 className="text-red-800 font-bold text-2xl">
            Server Connection Error!
          </h1>
        )}
        {/* Conversations Section */}
        {Conversations(data)}
        {/* Feedbacks Section */}
        {Feedbacks(feedbacks)}
      </div>
    </div>
  );
}

//* Components
function Conversations(data) {
  return (
    <section className="my-10 w-10/12 flex flex-col justify-start items-center">
      <h2 className="header2">Conversations</h2>
      <ul className="flex flex-row flex-wrap items-center justify-center gap-5">
        {data &&
          data
            .filter((item) => item.is_ended !== undefined && !item.is_ended)
            .map((item, index) => (
              <li key={index}>
                <Link
                  href={"/student/conversation/" + item["_id"]}
                  className="conversation-card"
                >
                  <h1 className="font-display text-lg">
                    Topic: {item["topic"]}
                  </h1>
                  <h2 className="font-display text-md">
                    Difficuly: {item["difficulty"]}
                  </h2>
                  <h2 className="font-display text-md">
                    Level: {item["user_level"]}
                  </h2>
                </Link>
              </li>
            ))}
      </ul>
    </section>
  );
}
// Feedbacks Section
function Feedbacks(data) {
  return (
    <section className="my-10 w-10/12 flex flex-col justify-start items-center">
      <h2 className="header2">Feedbacks</h2>
      <ul className="flex flex-row flex-wrap items-center justify-center gap-5">
        {data &&
          data.map((item, index) => (
            <li key={index}>
              <Link
                href={"/student/feedback/" + item["_id"]}
                className="feedback-card"
              >
                <h1 className="font-display text-lg">Topic: {item["topic"]}</h1>
                <h2 className="font-display text-md">
                  Difficuly: {item["difficulty"]}
                </h2>
                <h2 className="font-display text-md">
                  Level: {item["user_level"]}
                </h2>
              </Link>
            </li>
          ))}
      </ul>
    </section>
  );
}
