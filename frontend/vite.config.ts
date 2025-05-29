import path from "node:path";

import React from "@vitejs/plugin-react";
import UnoCSS from "unocss/vite";
import { defineConfig } from "vite";

export default defineConfig({
  server: { port: 8080 },
  resolve: { alias: { "~/": `${path.resolve(import.meta.dirname, "src")}/` } },
  plugins: [
    UnoCSS({ inspector: false }),
    React({
      babel: { plugins: [["babel-plugin-react-compiler", { target: "19" }]] },
    }),
  ],
  envPrefix: "SL__",
});
