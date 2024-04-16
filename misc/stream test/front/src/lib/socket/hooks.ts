/* eslint-disable react-hooks/exhaustive-deps */
import { useEffect, useMemo, useState } from "react";
import { socket } from ".";
import { EmitEventFunction, SendMessageFunction, SocketEventHandler } from "./types";



export function useSocket(handlers: SocketEventHandler[]): [boolean, string | undefined, EmitEventFunction, SendMessageFunction] {
    const eventHandlers = useMemo(() => [...handlers], [])
    const [isConnected, setIsConnected] = useState(socket.connected);
    const [connId, setConnId] = useState(socket.id)

    function sendMessage(data: any) {
        if (socket.connected)
            socket.send(data)
        else console.log("Socket is not conntected")
    }

    function emitEvent(key: string, data: any, callback?: (val: any) => void) {
        if (socket.connected)
            socket.emit(key, data, (val: any) => {
                callback?.(val)
            })
        else console.log("Socket is not connected")
    }

    useEffect(() => {
        function onConnect() {
            setIsConnected(true);
            setConnId(socket.id)
        }

        function onDisconnect() {
            setIsConnected(false);
            setConnId(undefined)
        }

        socket.on('connect', onConnect);
        socket.on('disconnect', onDisconnect);

        eventHandlers.forEach(eh => socket.on(eh.key, eh.handler))

        return () => {
            socket.off('connect', onConnect);
            socket.off('disconnect', onDisconnect);
            eventHandlers.forEach(eh => socket.off(eh.key, eh.handler))
        };
    }, []);

    return [isConnected, connId, emitEvent, sendMessage]
}
