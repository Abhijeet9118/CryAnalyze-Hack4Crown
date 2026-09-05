import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite configuration for GitHub Pages deployment and local dev
export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: '../docs',
    emptyOutDir: true,
  }
})
