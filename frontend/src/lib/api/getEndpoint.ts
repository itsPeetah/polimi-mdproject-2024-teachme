import resolveApiEndpoint from "./resolveApiEndpoint";

const ADDRESS = resolveApiEndpoint();

export default function getEndpoint(action: "register" | "login") {
  switch (action) {
    case "register":
      return `${ADDRESS}/register`;
    case "login":
      return `${ADDRESS}/login`;
  }
}
