import { defineConfig } from "vite";

export default defineConfig({
    base: "/dist/",
    server: {
       open: "/dist/src/templates/index.html",
    },
    build: {
        sourcemap: true,
        rollupOptions: {
            input: {
                //index: "src/ts/index.ts",
                index: "src/templates/index.html", // For using the dev server with HMR
            },
            output: {
                dir: "dist",
                assetFileNames: "[name].[ext]",
                entryFileNames: "[name].js",
            }
        }
    },
})
