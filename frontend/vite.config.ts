import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import pick from 'lodash/pick'

const PUBLIC_ENVIRONMENT_VARIABLES = [
  'API_BASE_URL',
]

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
    define: {
    'process.env': pick(process.env, PUBLIC_ENVIRONMENT_VARIABLES),
  },
});
