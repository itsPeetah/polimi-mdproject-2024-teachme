import resolveWebsocketEndpoint from "@/lib/ws/resolveWebsocketEndpoint";
import WebsocketProvider from "../../provider/WebsocketProvider";

/**
 * DO NOT USE THIS COMPONENT. This is only client side and should be used through the dynamic exported by ./index.tsx
 */
export default function AppUI() {
  return (
    <WebsocketProvider socketEndpoint={resolveWebsocketEndpoint()}>
      Student App UI
    </WebsocketProvider>
  );
}
