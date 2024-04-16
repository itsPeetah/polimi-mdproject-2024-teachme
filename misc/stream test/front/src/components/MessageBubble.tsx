import React, { ReactNode, useState } from "react";

export default function MessageBubble(props: {
  children: ReactNode;
  type: "user" | "chatbot";
}) {
  const { type, children } = props;
  const [ts] = useState(Date.now());
  const date = new Date(ts);
  const h = date.getHours();
  const m = date.getMinutes();
  const s = date.getSeconds();
  return (
    <div
      className={
        " p-1 rounded-md max-w-[400px]" +
        (type === "user"
          ? " ml-auto text-right bg-gray-400 text-black"
          : " mr-auto bg-sky-500 text-white")
      }
    >
      {children}
      <p className="text-xs opacity-50">
        {(h < 10 ? "0" : "") + h.toString()}:
        {(m < 10 ? "0" : "") + m.toString()}:
        {(s < 10 ? "0" : "") + s.toString()}
      </p>
    </div>
  );
}
