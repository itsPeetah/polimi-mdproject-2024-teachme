import dynamic from "next/dynamic";
import React from "react";

const App = dynamic(() => import("@/components/test/ChatAppTest"), {
  ssr: false,
  loading: () => (
    <div className="w-screen h-screen flex-col items-center justify-center">
      App Is Loading
    </div>
  ),
});

export default function Page() {
  return <App />;
}
