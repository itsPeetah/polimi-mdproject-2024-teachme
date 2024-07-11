import useTimer, { startTimer_global } from "@/lib/useTimer";
import { useEffect } from "react";

export default function Timer(props) {
  const { seconds, minutes, isDone } = useTimer(60 * props.duration, props.timerEnd);

  function formatSeconds(seconds) {
    return seconds < 10 ? "0" + seconds.toString() : seconds.toString();
  }

  useEffect(() => {
    if (props.isStart) {
      startTimer_global();
    }
  }, [props.isStart]);

  return (
    <div className="w-24 p-2 font-display text-lime-400 text-xl text-center border-2 border-lime-400 rounded-lg absolute top-6 right-10">
      {minutes}:{formatSeconds(seconds)}
    </div>
  );
}
