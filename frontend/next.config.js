/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8888/api/:path*',
      },
      {
        source: '/mock/:path*',
        destination: 'http://localhost:8888/mock/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
