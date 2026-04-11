export default defineConfig({
  server: {
    proxy: {
      "/api": {
        target: "https://sim2026q2-hexadev-production.up.railway.app",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
