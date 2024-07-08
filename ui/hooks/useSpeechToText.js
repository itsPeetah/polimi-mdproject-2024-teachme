import { useEffect, useState } from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

export default function useSpeechToText(stopWaitDurationMs, onStoppedSpeaking) {
  const {
    listening,
    transcript,
    interimTranscript,
    resetTranscript,
    browserSupportsSpeechRecognition,
    isMicrophoneAvailable,
  } = useSpeechRecognition();

  const [lastUpdateTs, setLastUpdateTS] = useState(0);
  const [timeoutId, setTimeoutId] = useState(null);
  const [pauseRequested, setPauseRequested] = useState(false);

  const speechRecognitionAvailable =
    browserSupportsSpeechRecognition && isMicrophoneAvailable;

  function startListening() {
    setPauseRequested(false);
    return SpeechRecognition.startListening({
      continuous: true,
      interimResults: true,
      language: "en-US",
    });
  }

  function stopListening() {
    return SpeechRecognition.stopListening();
  }

  function pauseRecognition() {
    setPauseRequested(true);
    if (timeoutId !== null) clearTimeout(timeoutId);
    setTimeoutId(null);
    stopListening().finally(() => {
      resetTranscript();
    });
  }

  useEffect(() => {
    if (!listening) return;

    function onTimeout() {
      console.log("[STT] Timeout");
      const now = Date.now();
      const diff = now - lastUpdateTs;
      if (diff >= stopWaitDurationMs) {
        console.log("[STT] User stopped talking");
        stopListening().finally(() => {
          console.log("[STT] Stopped listening");
          onStoppedSpeaking(transcript);
          resetTranscript();
        });
      }
    }

    if (!pauseRequested) {
      const tid = setTimeout(onTimeout, stopWaitDurationMs);
      if (timeoutId !== null) clearTimeout(timeoutId);
      setTimeoutId(tid);
    } else setPauseRequested(() => false);

    setLastUpdateTS(() => Date.now());
    console.log("Updated timestamp");
  }, [interimTranscript]);

  return {
    listening,
    speechRecognitionAvailable,
    transcript,
    startListening,
    stopListening,
    pauseRecognition,
  };
}
