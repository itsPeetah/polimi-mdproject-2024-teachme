import { useEffect, useState } from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

type UseSpeechToTextOption = {
  stopWaitDurationMs: number;
  onStoppedSpeaking?: (transcript: string) => void;
};

export default function useSpeechToText(options: UseSpeechToTextOption) {
  const { stopWaitDurationMs, onStoppedSpeaking } = options;
  const [lastChangeTs, setLastChangeTs] = useState(Date.now());
  const [isSpeaking, setIsSpeaking] = useState(false);

  const {
    transcript,
    interimTranscript,
    finalTranscript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
    isMicrophoneAvailable,
  } = useSpeechRecognition();

  function startListening() {
    SpeechRecognition.startListening({
      continuous: true,
      interimResults: true,
    });
  }

  function stopListening() {
    SpeechRecognition.stopListening();
  }

  useEffect(() => {
    if (!listening) return;

    const now = Date.now();
    if (!isSpeaking) setIsSpeaking(() => true);

    // Update last change and launch timeout
    setLastChangeTs(() => now);
    const timeoutId = setTimeout(() => {
      console.log("User stopped talking");
      setIsSpeaking(() => false);
      const text = transcript;
      resetTranscript();
      onStoppedSpeaking?.(text);
    }, stopWaitDurationMs);

    // Cleanup function to clear timeout on transcript change
    return () => clearTimeout(timeoutId);

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [interimTranscript]);

  return {
    // Speech recognition defaults
    transcript,
    interimTranscript,
    finalTranscript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
    isMicrophoneAvailable,
    // Hook customs
    startListening,
    stopListening,
    lastChangeTs,
    isSpeaking,
  };
}
