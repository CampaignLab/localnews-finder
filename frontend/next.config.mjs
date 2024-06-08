/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  images: {
    domains: ["imgs.search.brave.com", "news.google.com"],
  },
};

export default nextConfig;
