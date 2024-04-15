import { SERVER_URL } from "@/lib/constants";
import { RecordAudio } from "@/lib/medium/RecordAudio";
import React, { useState } from "react";

export default function AudioStreamer(props: { onData: (data: any) => void }) {
  const [recording, setRecording] = useState(false);
  const [audioRecorder, setAudioRecorder] = useState<RecordAudio | null>(null);

  const startRecording = () => {
    console.log("start recording");
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        console.log("stream available");
        const mr = new RecordAudio(stream);
        mr.addEventListener("stop", () => console.log("stopped"));
        mr.addEventListener("dataavailable", (data: any) => {
          props.onData(data);
        });
        mr.start(1000);
        setAudioRecorder(mr);
        setRecording(true);
      })
      .catch((err) => console.error("Error accessing microphone:", err));
  };

  const stopRecording = () => {
    console.log("stop recording");
    audioRecorder?.stop();
    setRecording(false);
  };

  return (
    <div className="flex flex-col gap-4">
      <h2>Audio recorder</h2>
      <p>Sends buffered data to websocket as &apos;audio_data&apos; events</p>
      <button onClick={recording ? stopRecording : startRecording}>
        {recording ? "Stop Recording" : "Start Recording"}
      </button>
      <button
        className="bg-amber-400 w-max"
        onClick={() => fetch(SERVER_URL + "/flush")}
      >
        Flush unsaved audio
      </button>
    </div>
  );
}
