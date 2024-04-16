import AudioStreamerDynamic from "@/components/AudioStreamerDynamic";
import React, { ReactNode, useState } from "react";
import { useSocket } from "../socket/hooks";
import MessageBubble from "@/components/MessageBubble";

export default function AppUI() {
  const [isConnected, connectionId, emitEvent, sendMessage] = useSocket([
    {
      key: "speaking_status",
      handler: (d) => console.log(d),
    },
    {
      key: "generic_data",
      handler: (d) => console.log("Received generic data", d),
    },
    {
      key: "transcript",
      handler: handleTranscriptEvent,
    },
  ]);

  const [messages, setMessages] = useState<ReactNode[]>([]);

  function sendAudioData(data: string) {
    console.log("sending audio data");
    emitEvent("audio_data", data, (val) => console.log("server received data"));
  }

  function handleTranscriptEvent(data: { user?: string; chatbot?: string }) {
    console.log(data);
    const { user, chatbot } = data;
    const messagesToAdd: ReactNode[] = [];
    if (user) {
      messagesToAdd.push(
        <MessageBubble key={user} type="user">
          {user}
        </MessageBubble>
      );
    }
    if (chatbot) {
      messagesToAdd.push(
        <MessageBubble key={chatbot} type="chatbot">
          {chatbot}
        </MessageBubble>
      );
    }

    setMessages((prev) => [...prev, ...messagesToAdd]);
  }

  return (
    <>
      <h3 suppressHydrationWarning>Id: {connectionId}</h3>
      {/* <AudioStreamer onData={sendAudioData} /> */}
      <AudioStreamerDynamic onData={sendAudioData} />
      <div className="flex flex-col w-full gap-4">
        <h1 className="text-center">Chat</h1>
        {messages}
      </div>
    </>
  );
}
