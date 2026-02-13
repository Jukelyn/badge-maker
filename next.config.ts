import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  devIndicators: false,
  output: "standalone",
};

export default nextConfig;
