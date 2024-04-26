/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async redirects() {
    return [
      {
        source: "/login",
        destination: "/auth/login",
        permanent: true,
      },
      {
        source: "/register",
        destination: "/auth/register",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
