import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: './', // Ensures relative assets load on GitHub Pages
  build: {
    outDir: '../docs', // Output production build into docs/ folder for GitHub Pages
    emptyOutDir: true,
  }
})
