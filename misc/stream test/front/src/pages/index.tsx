import Image from "next/image";
import { Inter } from "next/font/google";
import { useSocket } from "@/lib/socket/hooks";
import AudioStreamer from "@/components/AudioStreamer";
import dynamic from "next/dynamic";
import AudioStreamerDynamic from "@/components/AudioStreamerDynamic";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const [isConnected, connectionId, emitEvent, sendMessage] = useSocket([
    {
      key: "speaking_status",
      handler: (d) => console.log(d),
    },
    {
      key: "generic_data",
      handler: (d) => console.log("Received generic data", d),
    },
  ]);

  function sendAudioData(data: string) {
    console.log("sending audio data");
    emitEvent("audio_data", data, (val) => console.log("server received data"));
  }

  return (
    <main
      className={`flex min-h-screen flex-col gap-4 p-24 ${inter.className}`}
    >
      <h3 suppressHydrationWarning>Id: {connectionId}</h3>

      <button onClick={() => sendMessage("Hello, World")} type="button">
        Send &apos;Hello, world&apos; message
      </button>
      <button onClick={() => sendMessage("Hello, SocketIO")} type="button">
        Send &apos;Hello, SocketIO&apos; message
      </button>
      <button onClick={() => sendMessage({ hello: "World" })} type="button">
        Send &apos;Hello, world&apos; json
      </button>
      <button onClick={() => sendMessage({ hello: "SocketIO" })} type="button">
        Send &apos;Hello, SocketIO&apos; json
      </button>
      <button
        onClick={() =>
          emitEvent("foo", { foo: "bar" }, (v) => console.log("foo ack"))
        }
        type="button"
      >
        Emit &apos;foo&apos; event
      </button>
      {/* <AudioStreamer onData={sendAudioData} /> */}
      <AudioStreamerDynamic onData={sendAudioData} />
    </main>
  );
}
