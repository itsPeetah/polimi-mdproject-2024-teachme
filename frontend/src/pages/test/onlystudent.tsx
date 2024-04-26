import withAuthentication from "@/lib/server/withAuthentication";
import { GetServerSidePropsContext } from "next";

export default function onlystudent() {
  return <div>onlystudent</div>;
}

export const getServerSideProps = (ctx: GetServerSidePropsContext) =>
  withAuthentication(
    ctx,
    async (_ctx: GetServerSidePropsContext) => {
      return { props: {} };
    },
    "student"
  );
