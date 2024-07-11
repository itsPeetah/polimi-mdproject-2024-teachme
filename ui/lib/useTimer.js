import { useEffect, useState, useRef } from "react";

export default function useTimer(durationInSeconds, onTimerEnd) {
  const [remainingTime, setRemainingTime] = useState(durationInSeconds);
  const [isDone, setIsDone] = useState(false);
  const intervalIdRef = useRef(null);

  function start() {
    if (intervalIdRef.current !== null) {
      console.log(
        "[timer] timer is already running, cannot start another",
        intervalIdRef.current
      );
      return;
    }

    const onInterval = () => setRemainingTime((old) => old - 1);

    const iid = setInterval(onInterval, 1000);
    intervalIdRef.current = iid;
  }

  useEffect(() => {
    console.log("Interval id is", intervalIdRef.current);
  }, [intervalIdRef.current]);

  function pause() {
    if (intervalIdRef.current === null) {
      console.log(
        "[timer] can't pause since it's not been started",
        intervalIdRef.current
      );
      return;
    }

    clearInterval(intervalIdRef.current);
    intervalIdRef.current = null;
  }

  useEffect(() => {
    if (typeof window === "undefined") return;

    function onPause() {
      pause();
    }

    function onResume() {
      start();
    }

    window.addEventListener("timer.pause", onPause);
    window.addEventListener("timer.start", onResume);

    return () => {
      window.removeEventListener("timer.pause", onPause);
      window.removeEventListener("timer.start", onResume);
    };
  }, []);

  useEffect(() => {
    if (remainingTime <= 0) {
      pause();
      setIsDone(true);
      onTimerEnd();
    }
  }, [remainingTime]);

  const minutes = Math.floor(remainingTime / 60);
  const seconds = remainingTime - 60 * minutes;

  return { seconds, minutes, isDone };
}

export function startTimer_global() {
  window?.dispatchEvent(new Event("timer.start"));
}

export function pauseTimer_global() {
  window?.dispatchEvent(new Event("timer.pause"));
}
