export default defineConfig({
  server: {
    proxy: {
      "/api": {
        target: "http://backendapi",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
