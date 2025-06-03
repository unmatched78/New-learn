import type { Config } from 'tailwindcss'
import flowbite from 'flowbite/plugin'

export default {
  content: [
    './index.html',
    './src/**/*.{vue,ts,tsx}',
    './node_modules/flowbite/**/*.{js,ts}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2563eb',
        secondary: '#1f2937',
      },
    },
  },
  plugins: [
    flowbite,
  ],
} satisfies Config