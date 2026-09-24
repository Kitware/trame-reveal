export default {
  base: "./",
  build: {
    lib: {
      entry: "./src/main.js",
      name: "trame_revealjs",
      formats: ["umd"],
      fileName: "trame_revealjs",
    },
    rollupOptions: {
      external: ["vue"],
      output: {
        globals: {
          vue: "Vue",
        },
      },
    },
    outDir: "../src/trame_reveal/module/serve",
    assetsDir: ".",
  },
};
