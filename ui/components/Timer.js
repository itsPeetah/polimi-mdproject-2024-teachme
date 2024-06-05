import { useEffect } from 'react';
import { useTimer } from 'react-timer-hook';

export default function Timer(props) {
    const time = new Date();
    time.setSeconds(time.getSeconds() + 60 * props.duration);
    const {
        seconds, minutes, isRunning, start, pause, resume,
    } = useTimer({
        expiryTimestamp: time,
        autoStart: false,
        onExpire: () => {
            console.log('Timer Expired')
            props.timerEnd()
        }
    });
    useEffect(() => {
        if (props.isStart) {
            start()
        }
    }, [props.isStart, start])
    
    return (
        <div
            className='w-24 p-2 font-display text-lime-400 text-xl text-center border-2 border-lime-400 rounded-lg absolute top-6 right-10'
        >
            {minutes}:{seconds}
        </div>
    )
}