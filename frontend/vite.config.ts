import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const base = process.env.NODE_ENV === "production" ? "/TokiPona/" : "/"

// https://vitejs.dev/config/
export default defineConfig({
  base,
  plugins: [vue()],
  server:{
    proxy: {
      "/api": {
        target: "http://localhost:5000",
        rewrite: path => path.replace(/^\/api/, ""),
        changeOrigin:true
      }
    }
  }
})
