import Head from "next/head";
import { useRouter } from "next/router";
import { useState, useEffect } from "react";
import ReactMarkdown from 'react-markdown';
import useSWR from "swr";

export default function FeedbackPage() {
    // Constants
    const router = useRouter();
    const fetcher = (...args) => fetch(...args).then((res) => res.json())
    // States
    const [id, setId] = useState('');
    const [conversationInfo, setConversationInfo] = useState({
        topic: '',
        difficulty: '',
        userLevel: '',
        teacher: ''
    });
    const [overallFeedback, setOverallFeedback] = useState('');
    const [details, setDetails] = useState([{}]);
    const [isError, setIsError] = useState(false);
    // Get Conversation ID from URL
    useEffect(() => {
        if (router.isReady) {
            setId(router.query.id);
        }
    }, [router.isReady, router.query.id]);

    // Get Conversation Info
    const url = 'http://127.0.0.1:5000/get-conversation-info/' + id
    const { data, error } = useSWR(id ? url : null, fetcher)
    useEffect(() => {
        if (data) {
            setConversationInfo({
                topic: data['topic'],
                difficulty: data['difficulty'],
                userLevel: data['user_level'],
                teacher: data['teacher_email']
            });
            setIsError(false)
        } else if (error) {
            setIsError(true);
        }
    }, [data, error]);

    // Fetch feedback data
    useEffect(() => {
        const feedbackUrl = 'http://127.0.0.1:5000/post-conversation-info/' + id
        id && fetch(feedbackUrl)
            .then(response => response.json())
            .then(
                data => {
                    setOverallFeedback(data['overall_feedback'])
                    setDetails(data['messages'])
                }
            )
            .catch(error => setIsError(true));
    }, [id]);

    // Render
    return (
        <div className="min-h-screen px-8 py-10 flex flex-col items-center gap-10 bg-gradient-to-br from-sky-700  to-slate-900 "
        >
            <Head>
                <title>TeachMe | Feedback</title>
            </Head>
            <h1 className="header1">Feedback</h1>
            {/* Error Message */}
            {isError && (
                <p className="p-4 mb-8 text-red-500">
                    Error: Unable to Connect to the server
                </p>
            )}
            {/* Conversation Info */}
            {/*ConversationInfo(conversationInfo)*/}
            {/* Overall FeedBack */}
            {OverallFeedBack(overallFeedback)}
            {/* Details */}
            {Details(details)}
            {/* Back Button */}
            <button
                onClick={() => router.push('/student')}
                className="orange-btn w-1/3"
            >
                Close
            </button>
        </div>
    );
};

function ConversationInfo(conversationInfo) {
    return (
        <div className="glass-container">
            <h2 className="header2">Conversation Detail</h2>
            {Object.keys(conversationInfo).map((info, index) => {
                return (
                    <div key={index} className=" w-full flex gap-1 mb-3 font-display text text-xl">
                        <span className="w-32 font-bold capitalize">{info}: </span>
                        {conversationInfo[info]}
                    </div>
                )
            })}
        </div>
    )
}

function OverallFeedBack(overallFeedback) {
    return (
        <div className="glass-container">
            <h2 className="header2">
                Overall Feedback
            </h2>
            <ReactMarkdown className="sm:text-justify">
                {overallFeedback}
            </ReactMarkdown>
        </div>
    )
}

function Details(details) {
    return (
        <div className="glass-container">
            <h2 className="header2">Details</h2>
            <div className="flex flex-col justify-start">
                {details.map((detail, index) => {
                    return (
                        <div key={index} className="flex flex-col mb-6">
                            {detail['role'] === 'ai'
                                ? (
                                    <p className="font-mono mb-2">
                                        <span className="font-bold">
                                            AI Response:
                                        </span> {detail['message_content']}
                                    </p>
                                )
                                : (
                                    <div className="flex flex-col gap-5">
                                        <h3 className="header3 mb-2 text-lime-500">
                                            Message {index / 2 + 1}:
                                        </h3>
                                        <p>
                                            <span className="font-bold"> Content: </span>
                                            {detail['message_content']}
                                        </p>
                                        <p>
                                            <span className="font-bold"> Feedback: </span>
                                            {detail['feedback'] &&
                                                detail['feedback']['messageFeedback']}
                                        </p>
                                        <p>
                                            <span className="font-bold"> Synonyms: </span>
                                            {detail['synonyms'] &&
                                                detail['synonyms'].join(', ')}
                                        </p>
                                        <p>
                                            <span className="font-bold"> pronunciation: </span>
                                            {detail['pronunciation'] &&
                                                detail['pronunciation'].join(', ')}
                                        </p>
                                    </div>
                                )}
                        </div>
                    );
                })}
            </div>
        </div>
    )
}