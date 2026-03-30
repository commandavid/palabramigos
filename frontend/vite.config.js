import { definePlugin } from 'vite'
import react from '@vitejs/plugin-react'

export default {
  base: '/scrabble-solver/',   // must match your repo name exactly
  plugins: [react()],
}
```

**`.env.production`** — create this file inside `frontend/`. Vite will use it automatically when building for production:
```
VITE_API_URL=https://YOUR-RENDER-APP-NAME.onrender.com