import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Head from 'next/head';
// APIs
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import useSWR from 'swr';
import { getCookie } from 'cookies-next';
import { FiPlay, FiPause, FiStopCircle, FiLogOut } from 'react-icons/fi';
import 'animate.css'
// Components
import Mimi from "@/components/Mimi"
import Timer from '@/components/Timer';

export default function ConversationPage() {
    // Import Lottie Player
    useEffect(() => {
        import("@lottiefiles/lottie-player");
    });
    // Constants
    const router = useRouter()
    const userID = getCookie('id')
    const fetcher = (...args) => fetch(...args).then((res) => res.json())
    // Refrences
    const mimiRef = useRef(null)
    const lottieRef = useRef(null);
    // States
    const [topic, setTopic] = useState('')
    const [userLevel, setUserLevel] = useState('')
    const [id, setId] = useState('')
    const [isError, setIsError] = useState(false)
    const [isPlaying, setIsPlaying] = useState(true);
    const [isStart, setIsStart] = useState(false);
    const [isEnd, setIsEnd] = useState(false);
    const [duration, setDuration] = useState();
    // Voice Input
    const {
        transcript,
        finalTranscript,
        listening,
        resetTranscript,
        browserSupportsSpeechRecognition
    } = useSpeechRecognition();

    //* Effects
    // Check Browser Support for Speech Recognition
    useEffect(() => {
        if (!browserSupportsSpeechRecognition) {
            console.log('Browser doesnt support speech recognition.')
        }
    }, [browserSupportsSpeechRecognition])

    // Get Conversation ID from URL
    useEffect(() => {
        if (router.isReady) {
            setId(router.query.id);
        }
    }, [router.isReady, router.query.id]);

    // Start Listening
    useEffect(() => {
        if (!isPlaying && !isEnd) {
            SpeechRecognition.startListening({
                continuous: false,
                language: 'en-US'
            })
        }
    }, [isEnd, isPlaying])

    //* Functions 
    // Handle Audio Play
    const handleAudioPlay = (status) => {
        setIsPlaying(status);
    };

    const handleTimerEnd = () => {
        setIsEnd(true)
    }

    // Begin Conversation
    const begin = () => {
        setIsStart(true);
        setIsPlaying(false);
    }

    // Activate Mimi function
    const activateMimi = (script, userLevel) => {
        const voice = 'en-US-JennyNeural'
        const pitch = '0%'
        let rate = '0%'
        if (userLevel === 'beginner') {
            rate = '0%'
        } else if (userLevel === 'intermediate') {
            rate = '10%'
        }
        else if (userLevel === 'advanced') {
            rate = '20%'
        }
        mimiRef.current.activeMimi(voice, script, rate, pitch)
    }

    //* REST APIs
    // Get Conversation Info
    const url = 'http://127.0.0.1:5000/get-conversation-info/' + id
    const { data, error } = useSWR(id ? url : null, fetcher)
    useEffect(() => {
        if (data) {
            setTopic(data['topic'])
            setUserLevel(data['user_level'])
            setDuration(data['time_limit'])
            setIsError(false)
        } else if (error) {
            setIsError(true);
        }
    }, [data, error]);

    // Initialize Conversation
    const url2 = 'http://127.0.0.1:5000/initialize-conversation'
    useEffect(() => {
        async function init() {
            const initRes = await fetch(url2, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    'conversation_id': id
                })
            })
            if (!initRes.ok) {
                console.log('Error initializing conversation.')
                setIsError(true)
            } else {
                console.log('Conversation initialized.')
                setIsError(false)
            }
        }
        id && init()
    }, [id])

    // Conversation Handler
    const url3 = 'http://127.0.0.1:5000/user-chat-message'
    useEffect(() => {
        if (finalTranscript && !listening && !isError) {
            console.log('Transcript:', finalTranscript)
            async function conversationHandler() {
                const res = await fetch(url3, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        'conversation_id': id,
                        "sender_id": userID,
                        "message": finalTranscript
                    })
                })
                if (res.ok) {
                    console.log('Conversation send.')
                    const data = await res.json()
                    // Activate Mimi
                    activateMimi(data['response'], userLevel)
                    console.log('Mimi activated.')
                    //Reset transcript
                    resetTranscript()
                } else {
                    console.log('Error sending conversation.')
                }
            }
            conversationHandler()
        }
    }, [finalTranscript, id, listening, resetTranscript, userID, isPlaying, isError, userLevel])

    // End Conversation
    const endConversation = () => {
        const url4 = 'http://127.0.0.1:5000/end-conversation/' + id
        fetch(url4)
            .then((res) => {
                if (res.ok) {
                    console.log('Conversation ended.')
                    router.push('/student')
                } else {
                    console.log('Error ending conversation.')
                    setIsError(true)
                }
            })
            .catch((error) => { setIsError(true) })
    }

    // RENDER
    return (
        <div
            className="flex flex-col justify-start items-center h-screen p-8 text-white overflow-y-scroll bg-gradient-to-bl from-indigo-500 via-indigo-800 to-slate-900"
        >
            <Head>
                <title>TeachMe | Conversation</title>
            </Head>
            {/* Heading */}
            <h1 className='header2'>{'Lets talk about \"' + topic + '\"'}</h1>
            {/* Timer */}
            {duration && <Timer duration={duration} timerEnd={handleTimerEnd} isStart={isStart} />}
            {/* Error */}
            {isError && <h1 className="text-rose-800 font-bold text-2xl">Server Error!</h1>}
            {/* MIMI */}
            <div className='mt-4'>
                <Mimi ref={mimiRef} onPlayAudio={handleAudioPlay} />
            </div>
            {/* Start Button */}
            {!isStart && StartBtns(begin)}
            {/* Mic Listening Indicator */}
            {isStart && Listening(listening, lottieRef)}
            {/* Toolbar */}
            {isStart && !isEnd && Toolbar()}
            {/* End Button */}
            {isEnd &&
                <button className='orange-btn' onClick={endConversation}>
                    End Conversation
                </button>
            }
        </div > // End of Main Container
    );
};

//* Components
function Listening(listening, lottieRef) {
    return (
        <div className={'my-10 w-44 ' + (listening ? 'visible' : 'invisible')}>
            <lottie-player
                src='/lottie/mic.json'
                ref={lottieRef}
                loop autoplay />
        </div>
    );
}

function StartBtns(start) {
    return (
        <div className='flex flex-col justify-center items-center gap-14'>
            <button
                className='start-btn animate__animated animate__pulse animate__infinite'
                onClick={start}
            >
                Start
            </button>
            <Link className='navigation-btn w-36' href='/student'>
                Back
            </Link>
        </div>
    );
}

function Toolbar() {
    return (
        <div
            className='flex flex-row gap-10 px-4 sm:px-10 py-6 mt-auto mb-4 rounded-full shadow-inner bottom-10 bg-slate-800 shadow-slate-700'
        >
            {/* play button */}
            <button
                onClick={() => {
                    SpeechRecognition.startListening({
                        continuous: false,
                        language: 'en-US'
                    })
                }}
            >
                <FiPlay size={26} />
            </button>
            {/* pause button */}
            <button onClick={SpeechRecognition.abortListening}>
                <FiPause size={26} />
            </button>
            {/* stop listening button */}
            <button onClick={SpeechRecognition.stopListening}>
                <FiStopCircle size={26} />
            </button>
            {/* exit button */}
            <Link href="/student">
                <FiLogOut size={26} />
            </Link>
        </div>
    );
}