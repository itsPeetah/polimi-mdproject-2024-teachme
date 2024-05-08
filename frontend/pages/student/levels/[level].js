import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { FiChevronRight, FiChevronLeft, FiRepeat, FiPlay, FiPause, FiMic, FiMicOff, FiStopCircle } from 'react-icons/fi';
import 'animate.css';
// Components
import getData from '@/services/getData';
import { HeadingL, HeadingXL } from '@/components/headings';
import { SideMenuBtn } from '@/components/buttons';

export async function getStaticPaths() {
  return {
    paths: [
      { params: { level: 'A1' } },
      { params: { level: 'A2' } },
      { params: { level: 'B1' } },
      { params: { level: 'B2' } },
      { params: { level: 'C1' } },
      { params: { level: 'C2' } },
    ],
    fallback: false, // false or "blocking"
  }
}

export async function getStaticProps() {
  const data = await getData()
  return { props: { data } }
}

export default function Level({ data }) {
  // Level and Lessons Data
  const router = useRouter()
  let level = router.query.level;
  const lessons = data[level].lessons;
  const [lesson, setLesson] = useState(lessons[0])
  const changeLesson = (lesson) => {
    setLesson(lesson)
  };

  // Side-Menu Handler
  const [showMenu, setShowMenu] = useState(true);
  const toggleMenu = () => {
    setShowMenu(!showMenu);
  };

  // Voice Input
  const {
    transcript,
    finalTranscript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition
  } = useSpeechRecognition();
  useEffect(() => {
    if (!browserSupportsSpeechRecognition) {
      console.log('Browser doesnt support speech recognition.')
    }
  }, [browserSupportsSpeechRecognition])

  return (
    <div
      className="flex h-screen overflow-y-scroll bg-gradient-to-bl from-indigo-500 via-indigo-800 to-slate-900"
    >
      {/* Toggle Side-Menu Button*/}
      <button
        onClick={toggleMenu}
        className="relative z-50 h-full p-4 text-white border-r-2 bg-slate-900/40 backdrop-blur-lg border-slate-600"
      >
        {showMenu ? <FiChevronLeft size={24} /> : <FiChevronRight size={24} />}
      </button>
      {/* Side-Menu */}
      <div
        className={`
          bg-slate-900/40 backdrop-blur-lg text-white
          p-8 w-full lg:w-80 h-full
          transition-all duration-300 ease-linear
          overflow-y-scroll
          animate__animated
          ${showMenu
            ? 'left-0 animate__slideInLeft absolute lg:sticky'
            : 'animate__slideOutLeft absolute'
          }
          `
        }
      >
        <HeadingL text={'Lessons'} />
        <ul>
          {lessons.map((lesson, index) =>
            <li key={index} className='mb-10'>
              <SideMenuBtn text={lesson} action={() => changeLesson(lesson)} />
            </li>
          )}
        </ul>
      </div>

      {/* Main Section */}
      <div className="flex flex-col items-center justify-start flex-1 p-8 text-white">
        <HeadingXL text={lesson} />
        {/* Main content */}
        <div className='self-start w-2/5 p-4 rounded-lg backdrop-blur bg-slate-900/60'>
          <p>Transcript: {transcript}</p>
        </div>
        <div className='self-end w-2/5 p-4 rounded-lg backdrop-blur bg-purple-900/80'>
          <p>Response:</p>
        </div>
        {/* Voice Input */}
        <div className='fixed flex flex-row gap-10 p-6 rounded-full shadow-inner bottom-10 bg-slate-800 shadow-slate-700'
        >
          {listening ? <FiMic size={24} /> : <FiMicOff size={24} />}
          <button
            onClick={
              () => SpeechRecognition.startListening({ continuous: true, language: 'en-US' })
            }
          >
            <FiPlay size={24} />
          </button>
          <button onClick={SpeechRecognition.stopListening}>
            <FiPause size={24} />
          </button>
          <button onClick={SpeechRecognition.abortListening}>
            <FiStopCircle size={24} />
          </button>
          <button onClick={resetTranscript}>
            <FiRepeat size={24} />
          </button>
        </div>
      </div>
    </div>

  );
};
