import resolveApiEndpoint from "./resolveApiEndpoint";

const ADDRESS = resolveApiEndpoint();

export default function getEndpoint(action: "register" | "login" | "me") {
  switch (action) {
    case "register":
      return `${ADDRESS}/register`;
    case "login":
      return `${ADDRESS}/login`;
    case "me":
      return `${ADDRESS}/me`;
  }
}
