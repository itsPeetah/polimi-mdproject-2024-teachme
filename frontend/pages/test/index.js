import { useEffect } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { FiRepeat, FiPlay, FiPause, FiSquare, FiMic, FiMicOff, FiX } from 'react-icons/fi';
const Dictaphone = () => {
    const {
        transcript,
        listening,
        resetTranscript,
        browserSupportsSpeechRecognition
    } = useSpeechRecognition();

    useEffect(() => {
        if (!browserSupportsSpeechRecognition) {
            return <div><p>Browser doesnt support speech recognition.</p></div>;
        }
    }, [browserSupportsSpeechRecognition])

    return (
        <div className='flex justify-center min-h-screen'>
            <div className='fixed flex flex-row gap-10 p-6 rounded-full bottom-10 bg-slate-500/50 backdrop-blur-md'>
                {listening ? <FiMic size={24}/> : <FiMicOff size={24}/>}
                <button onClick={SpeechRecognition.startListening}><FiPlay size={24}/></button>
                <button onClick={SpeechRecognition.stopListening}><FiPause size={24}/></button>
                <button onClick={SpeechRecognition.abortListening}><FiX size={24}/></button>
                <button onClick={resetTranscript}><FiRepeat size={24}/></button>
            </div>
            <h1>{transcript}</h1>
        </div>
    );
};
export default Dictaphone;