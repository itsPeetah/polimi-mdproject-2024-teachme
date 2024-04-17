import React, { ReactNode, useEffect, useState } from "react";
import WebsocketProvider, { useWebsocket } from "../provider/WebsocketProvider";
import resolveWebsocketEndpoint from "@/lib/ws/resolveWebsocketEndpoint";
import useSpeechToText from "@/lib/media/speech/useSpeechToText";

const socketEndpoint = resolveWebsocketEndpoint();

export default function ChatAppTest() {
  return (
    <WebsocketProvider socketEndpoint={socketEndpoint}>
      <AppContent />
    </WebsocketProvider>
  );
}

function AppContent() {
  const { isConnected, socket } = useWebsocket();
  const { startListening } = useSpeechToText({
    stopWaitDurationMs: 3000,
    onStoppedSpeaking: onStoppedSpeaking,
  });

  const [messages, setMessages] = useState<ReactNode[]>([]);

  function onStoppedSpeaking(transcript: string) {
    setMessages((previous) => [
      ...previous,
      <MessageBubble key={transcript} type="user">
        {transcript}
      </MessageBubble>,
    ]);
    socket.emit("transcript_data", transcript);
  }

  function onChatbotResponse(response: string) {
    setMessages((previous) => [
      ...previous,
      <MessageBubble key={response} type="chatbot">
        {response}
      </MessageBubble>,
    ]);
  }

  useEffect(() => {
    socket.on("chatbot_response", onChatbotResponse);
    return () => {
      socket.off("chatbot_response", onChatbotResponse);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="w-full min-h-screen flex flex-col gap-4 p-4">
      <button onClick={() => startListening()}>Start Chatting!</button>
      <div className=" w-full max-w-[800px] h-full flex flex-col gap-4  mx-auto bg-slate-200">
        <h1 className="text-center">Chat</h1>
        {messages}
      </div>
    </div>
  );
}

function MessageBubble(props: {
  children: ReactNode;
  type: "user" | "chatbot";
}) {
  const { type, children } = props;
  const [ts] = useState(Date.now());
  const date = new Date(ts);
  const h = date.getHours();
  const m = date.getMinutes();
  const s = date.getSeconds();
  return (
    <div
      className={
        " p-1 rounded-md max-w-[400px]" +
        (type === "user"
          ? " ml-auto text-right bg-gray-400 text-black"
          : " mr-auto bg-sky-500 text-white")
      }
    >
      {children}
      <p className="text-xs opacity-50">
        {(h < 10 ? "0" : "") + h.toString()}:
        {(m < 10 ? "0" : "") + m.toString()}:
        {(s < 10 ? "0" : "") + s.toString()}
      </p>
    </div>
  );
}
