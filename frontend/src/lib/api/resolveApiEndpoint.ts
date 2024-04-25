import { API_ADDRESS_DEV, API_ADDRESS_PROD } from "../constants";

export default function resolveApiEndpoint() {
  return process.env.NODE_ENV === "production"
    ? API_ADDRESS_PROD
    : API_ADDRESS_DEV;
}
