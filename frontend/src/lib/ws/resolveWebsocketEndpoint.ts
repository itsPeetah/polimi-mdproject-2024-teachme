import {
  STUDENT_WEBSOCKET_ENPOINT_DEV,
  STUDENT_WEBSOCKET_ENPOINT_PROD,
} from "../constants";

export default function resolveWebsocketEndpoint() {
  return process.env.NODE_ENV === "production"
    ? STUDENT_WEBSOCKET_ENPOINT_PROD
    : STUDENT_WEBSOCKET_ENPOINT_DEV;
}
