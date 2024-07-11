import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import Head from "next/head";
// APIs
import useSWR from "swr";
import { getCookie } from "cookies-next";
import { FiPlay, FiPause, FiStopCircle, FiLogOut } from "react-icons/fi";
import "animate.css";
// Components
import Mimi from "@/components/Mimi";
import Timer from "@/components/Timer";
import useSpeechToText from "@/lib/useSpeechToText";
import { pauseTimer_global, startTimer_global } from "@/lib/useTimer";
import { BACKEND_URL_BASE } from "@/lib/constants";

const LISTEN_START_OPTIONS = {
  language: "en-US",
  // continuous: true,
  interimResults: true,
};

export default function ConversationPage() {
  // Import Lottie Player
  useEffect(() => {
    import("@lottiefiles/lottie-player");
  });
  // Constants
  const router = useRouter();
  const userID = getCookie("id");
  const fetcher = (...args) => fetch(...args).then((res) => res.json());
  // Refrences
  const mimiRef = useRef(null);
  const lottieRef = useRef(null);
  // States
  const [topic, setTopic] = useState("");
  const [userLevel, setUserLevel] = useState("");
  const [id, setId] = useState("");
  const [isError, setIsError] = useState(false);
  const [isPlaying, setIsPlaying] = useState(true);
  const [isStart, setIsStart] = useState(false);
  const [isEnd, setIsEnd] = useState(false);
  const [duration, setDuration] = useState();

  const {
    listening,
    speechRecognitionAvailable,
    transcript,
    startListening,
    stopListening,
    pauseRecognition,
  } = useSpeechToText(2500, handleUserStoppedTalking);

  //* Effects
  // Check Browser Support for Speech Recognition
  useEffect(() => {
    if (!speechRecognitionAvailable) {
      console.log("Browser doesnt support speech recognition.");
      console.log("Might also be that you don't have a mic :)");
    }
  }, [speechRecognitionAvailable]);

  // Get Conversation ID from URL
  useEffect(() => {
    if (router.isReady) {
      setId(router.query.id);
    }
  }, [router.isReady, router.query.id]);

  // Start Listening
  useEffect(() => {
    if (!isPlaying && !isEnd) {
      startListening();
    }
  }, [isEnd, isPlaying]);

  //* Functions
  // Handle Audio Play
  const handleAudioPlay = (status) => {
    setIsPlaying(status);
  };

  const handleTimerEnd = () => {
    setIsEnd(true);
  };

  // Begin Conversation
  const begin = () => {
    setIsStart(true);
    setIsPlaying(false);
  };

  // Activate Mimi function
  const activateMimi = (script, userLevel) => {
    const voice = "en-US-JennyNeural";
    const pitch = "0%";
    let rate = "0%";
    if (userLevel === "beginner") {
      rate = "0%";
    } else if (userLevel === "intermediate") {
      rate = "10%";
    } else if (userLevel === "advanced") {
      rate = "20%";
    }
    setIsPlaying(true); // This is troppo spaghetti D:
    mimiRef.current.activeMimi(voice, script, rate, pitch);
  };

  //* REST APIs
  // Get Conversation Info
  const url = `${BACKEND_URL_BASE}/get-conversation-info/${id}`;
  const { data, error } = useSWR(id ? url : null, fetcher);
  useEffect(() => {
    if (data) {
      setTopic(data["topic"]);
      setUserLevel(data["user_level"]);
      setDuration(data["time_limit"]);
      setIsError(false);
    } else if (error) {
      setIsError(true);
    }
  }, [data, error]);

  // Initialize Conversation
  const url2 = `${BACKEND_URL_BASE}/initialize-conversation`;
  useEffect(() => {
    async function init() {
      const initRes = await fetch(url2, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: id,
        }),
      });
      if (!initRes.ok) {
        console.log("Error initializing conversation.");
        setIsError(true);
      } else {
        console.log("Conversation initialized.");
        setIsError(false);
      }
    }
    id && init();
  }, [id]);

  // Conversation Handler
  const url3 = `${BACKEND_URL_BASE}/user-chat-message`;
  function handleUserStoppedTalking(userTranscript /* string */) {
    console.log("Handling user transcript");

    if (isError || isEnd) {
      console.log("There's a time and place for everything but not now...");
      return;
    }

    if (!userTranscript || userTranscript.length < 1) {
      console.log("No transcript?", userTranscript);
      return;
    }

    console.log("Transcript:", userTranscript);

    async function handleTranscript() {
      // Send POST req
      const res = await fetch(url3, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: id,
          sender_id: userID,
          message: userTranscript,
        }),
      });
      if (res.ok) {
        console.log("Conversation send.");
        const data = await res.json();
        // Activate Mimi
        activateMimi(data["response"], userLevel);
        console.log("Mimi activated.");
      } else {
        console.log("Error sending conversation.");
      }
    }

    handleTranscript();
  }

  // End Conversation
  const endConversation = () => {
    const url4 = `${BACKEND_URL_BASE}/end-conversation/${id}`;
    fetch(url4)
      .then((res) => {
        if (res.ok) {
          console.log("Conversation ended.");
          router.push("/student");
        } else {
          console.log("Error ending conversation.");
          setIsError(true);
        }
      })
      .catch((error) => {
        setIsError(true);
      });
  };

  // RENDER
  return (
    <div className="flex flex-col justify-start items-center h-screen p-8 text-white overflow-y-scroll bg-gradient-to-bl from-indigo-500 via-indigo-800 to-slate-900">
      <Head>
        <title>TeachMe | Conversation</title>
      </Head>
      {/* Heading */}
      <h1 className="header2">{'Lets talk about "' + topic + '"'}</h1>
      {/* Timer */}
      {duration && (
        <Timer
          duration={duration}
          timerEnd={handleTimerEnd}
          isStart={isStart}
        />
      )}
      {/* Error */}
      {isError && (
        <h1 className="text-rose-800 font-bold text-2xl">Server Error!</h1>
      )}
      {/* MIMI */}
      <div className="mt-4">
        <Mimi ref={mimiRef} onPlayAudio={handleAudioPlay} />
      </div>
      {/* Start Button */}
      {!isStart && StartBtns(begin)}
      {/* Mic Listening Indicator */}
      {isStart && (
        <Listening
          listening={listening}
          lottieRef={lottieRef}
          isPlaying={isPlaying}
        />
      )}
      {/* Toolbar */}
      {isStart && !isEnd && (
        <>
          <Toolbar
            functions={{ startListening, stopListening, pauseRecognition }}
          />
        </>
      )}
      {/* End Button */}
      {isEnd && (
        <button className="orange-btn" onClick={endConversation}>
          End Conversation
        </button>
      )}
    </div> // End of Main Container
  );
}

//* Components
function Listening({ listening, lottieRef }) {
  return (
    <div className={"my-10 w-44 " + (listening ? "visible" : "invisible")}>
      <lottie-player src="/lottie/mic.json" ref={lottieRef} loop autoplay />
    </div>
  );
}

function StartBtns(start) {
  return (
    <div className="flex flex-col justify-center items-center gap-14">
      <button
        className="start-btn animate__animated animate__pulse animate__infinite"
        onClick={start}
      >
        Start
      </button>
      <Link className="navigation-btn w-36" href="/student">
        Back
      </Link>
    </div>
  );
}

function Toolbar({ functions, ...props }) {
  return (
    <div className="flex flex-row gap-10 px-4 sm:px-10 py-6 mt-auto mb-4 rounded-full shadow-inner bottom-10 bg-slate-800 shadow-slate-700">
      {/* play button */}
      <button
        onClick={() => {
          functions.startListening();
          startTimer_global();
        }}
      >
        <FiPlay size={26} />
      </button>
      {/* pause button */}
      <button
        onClick={() => {
          functions.pauseRecognition();
          pauseTimer_global();
        }}
      >
        <FiPause size={26} />
      </button>
      {/* stop listening button */}
      <button onClick={() => functions.stopListening()}>
        <FiStopCircle size={26} />
      </button>
      {/* exit button */}
      <Link href="/student">
        <FiLogOut size={26} />
      </Link>
    </div>
  );
}
