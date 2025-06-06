import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/users': 'http://localhost:5000',
      '/api': 'http://localhost:5000',
      '/reviews': 'http://localhost:5000',
      '/products': 'http://localhost:5000',
    }
  }
})
