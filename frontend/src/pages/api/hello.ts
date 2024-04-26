// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import getEndpoint from "@/lib/api/getEndpoint";
import type { NextApiRequest, NextApiResponse } from "next";

type Data = {
  cookie: string;
  header: string;
};

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const ep = getEndpoint("me");
  fetch(ep, {
    credentials: "include",
    headers: {
      cookie: req.headers.cookie ?? "",
    },
  })
    .then((_res) => {
      if (_res.status !== 200) {
        res.status(200).send("lmao");
        return;
      }
      res.status(200).send("");
      return;
    })
    .catch((err) => {
      console.log("error");
      res.status(200).json(err);
      return;
    });
  // res.status(200).json({
  //   cookie: req.cookies["uid"] ?? "",
  //   header: req.headers.cookie ?? "",
  // });
}
