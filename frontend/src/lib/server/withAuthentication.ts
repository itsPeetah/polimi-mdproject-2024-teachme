import {
  GetServerSideProps,
  GetServerSidePropsContext,
  GetServerSidePropsResult,
} from "next";
import getEndpoint from "../api/getEndpoint";

export default async function withAuthentication(
  context: GetServerSidePropsContext,
  wrapped: GetServerSideProps,
  authRole?: "student" | "teacher"
) {
  const cookies = context.req.cookies["uid"];

  // if no cookie present
  if (cookies === undefined) {
    return {
      redirect: {
        destination: "/auth/login",
        permanent: false,
      },
    };
  }

  try {
    // Check auth
    const ep = getEndpoint("me");
    const me = await fetch(ep, {
      credentials: "include",
      headers: {
        cookie: context.req.headers.cookie ?? "",
      },
    });

    // if not logged in (cookie not valid)
    if (me.status !== 200) {
      //   context.req.cookies["uid"] = undefined;
      return {
        redirect: {
          destination: "/auth/login",
          permanent: false,
        },
      };
    }

    // check role
    const user = (await me.json()) as {
      user_id: string;
      role: "student" | "teacher";
    };
    if (authRole !== undefined && authRole != user.role) {
      return {
        redirect: {
          destination: "/",
          permanent: false,
        },
      };
    }
    // if match
    const wrappedResult = await wrapped(context);
    return wrappedResult;
  } catch (err) {
    return {
      redirect: {
        destination: "/auth/login",
        permanent: false,
      },
    };
  }
}
