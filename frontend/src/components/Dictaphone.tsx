import useSpeechToText from "@/lib/media/speech/useSpeechToText";

export default function Dictaphone() {
  const {
    startListening,
    stopListening,
    isSpeaking,
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
    interimTranscript,
    finalTranscript,
    isMicrophoneAvailable,
  } = useSpeechToText({
    stopWaitDurationMs: 5000,
    onStoppedSpeaking: handleStopSpeaking,
  });

  function handleStopSpeaking(text: string) {
    alert(text);
  }

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn&apos;t support speech recognition.</span>;
  }
  return (
    <div>
      <p>Is Speaking: {isSpeaking.toString()}</p>
      <p>Microphone: {listening ? "on" : "off"}</p>
      <button onClick={startListening}>Start</button>
      <button onClick={stopListening}>Stop</button>
      <button onClick={resetTranscript}>Reset</button>
      <h2>t</h2>
      <p>{transcript}</p>
      <h2>i t</h2>
      <p>{interimTranscript}</p>
      <h2>f t</h2>
      <p>{finalTranscript}</p>
    </div>
  );
}
