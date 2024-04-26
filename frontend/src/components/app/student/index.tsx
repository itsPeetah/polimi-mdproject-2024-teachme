import dynamic from "next/dynamic";

const StudentAppClientOnly = dynamic(() => import("./StudentAppContent"), {
  ssr: false,
  loading: () => <div>loading</div>,
});

export default function StudentAppUI() {
  return <StudentAppClientOnly />;
}
