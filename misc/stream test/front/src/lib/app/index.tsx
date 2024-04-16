import dynamic from "next/dynamic";

const ClientSideAppUI = dynamic(() => import("./AppUI"), {
  ssr: false,
  loading: () => <div>loading</div>,
});

export default ClientSideAppUI;
