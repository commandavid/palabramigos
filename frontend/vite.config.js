import { definePlugin } from 'vite'
import react from '@vitejs/plugin-react'

export default {
  base: '/palabramigos/',   // must match your repo name exactly
  plugins: [react()],
}

