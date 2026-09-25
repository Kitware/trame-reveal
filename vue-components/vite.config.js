import { cpSync } from "node:fs";
import { fileURLToPath } from "node:url";

const outDir = fileURLToPath(
  new URL("../src/trame_reveal/module/serve", import.meta.url),
);
const themeSrcDir = fileURLToPath(
  new URL("./node_modules/reveal.js/dist/theme", import.meta.url),
);

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
    outDir,
    assetsDir: ".",
  },
  plugins: [
    {
      name: "copy-reveal-theme",
      closeBundle() {
        cpSync(themeSrcDir, `${outDir}/theme`, { recursive: true });
      },
    },
  ],
};
