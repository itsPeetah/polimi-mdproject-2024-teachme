import dynamic from "next/dynamic";

const AudioStreamerDynamic = dynamic(() => import("./AudioStreamer"), { ssr: false })
export default AudioStreamerDynamic