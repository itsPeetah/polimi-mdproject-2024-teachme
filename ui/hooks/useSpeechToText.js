/**
 *  Taken from the previous tests and ported from ts to js (just had to comment out the type defs/decls)
 *  https://github.com/itsPeetah/polimi-mdproject-2024-teachme/blob/4a84f314050ba95d7e09fb4c666d151fa57e6d18/frontend/src/components/test/ChatAppTest.tsx
 */

import { useEffect, useState } from "react";
import { useSpeechRecognition } from "react-speech-recognition";

// type UseSpeechToTextOption = {
//   stopWaitDurationMs: number;
//   onStoppedSpeaking?: (transcript: string) => void;
// };

export default function useSpeechToText(options /*: UseSpeechToTextOption*/) {
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
    lastChangeTs,
    isSpeaking,
  };
}
