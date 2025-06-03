import type { Config } from 'tailwindcss'
import flowbite from 'flowbite/plugin'

export default {
  content: [
    './index.html',
    './src/**/*.{vue,ts,tsx}',
    './node_modules/flowbite/**/*.js', // Include Flowbite's JS files for class scanning
  ],
  theme: {
    extend: {},
  },
  plugins: [
    flowbite, // Use the imported Flowbite plugin
  ],
} satisfies Config