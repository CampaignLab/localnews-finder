/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  images: {
    unoptimized: true,
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**", // This allows images from any domain
      },
      {
        protocol: "http",
        hostname: "**", // This allows images from any domain
      },
    ],
  },
};

export default nextConfig;
