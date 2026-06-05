import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/users': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/products': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/sales': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/pricing': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/forecast': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/inventory': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/promotions': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    }
  }
})