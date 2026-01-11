/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'meta-bg': '#0a0a0c',
        'meta-card': 'rgba(23, 23, 27, 0.8)',
        'meta-accent': '#8b5cf6',
        'meta-accent-glow': 'rgba(139, 92, 246, 0.4)',
      },
      backgroundImage: {
        'meta-gradient': 'radial-gradient(circle at top right, #1e1b4b, #000000)',
      },
      backdropBlur: {
        'xs': '2px',
      }
    },
  },
  plugins: [],
}
