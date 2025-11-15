import { randomBytes } from 'crypto';
if (!globalThis.crypto) {
  globalThis.crypto = { getRandomValues: (arr) => randomBytes(arr.length) };
}

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: { port: 5173 },
  esbuild: { target: 'esnext' },
});
