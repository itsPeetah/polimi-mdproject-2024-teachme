import {
  ReactNode,
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { Socket, io } from "socket.io-client";

const WebsocketContext = createContext<{
  isConnected: boolean;
  socket: Socket;
} | null>(null);

export const useWebsocket = () => {
  return useContext(WebsocketContext)!;
};

interface WebsocketProviderProps {
  socketEndpoint: string;
  children?: ReactNode;
}

export default function WebsocketProvider({
  socketEndpoint,
  children,
}: WebsocketProviderProps) {
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const socket = useMemo(() => io(socketEndpoint, { autoConnect: false }), []);
  const [isConnected, setIsConnected] = useState(false); // this is a stupid hack to get the rerender when socket updates internally

  useEffect(() => {
    function onConnect() {
      console.log("Socket connection established.", socket.id);
      setIsConnected(socket.connected);
    }
    function onDisconnect() {
      console.log("Socket connection terminated.", socket.id);
      setIsConnected(socket.connected);
    }

    socket.on("connect", onConnect);
    socket.on("disconnect", onDisconnect);

    socket.connect();

    return () => {
      socket.off("connect", onConnect);
      socket.off("disconnect", onDisconnect);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <WebsocketContext.Provider value={{ socket, isConnected }}>
      {children}
    </WebsocketContext.Provider>
  );
}
