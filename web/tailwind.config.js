/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'meta-bg': 'var(--bg-app)',
        'meta-panel': 'var(--bg-panel)',
        'meta-surface': 'var(--bg-surface)',
        'meta-surface-hover': 'var(--bg-surface-hover)',
        'meta-card': 'var(--bg-surface)', 
        
        'meta-main': 'var(--text-main)',
        'meta-muted': 'var(--text-muted)',
        
        'meta-border': 'var(--border-subtle)',
        'meta-border-strong': 'var(--border-strong)',
        
        'meta-accent': 'var(--color-accent)',
        'meta-accent-glow': 'var(--color-accent-glow)',
      },
      backgroundImage: {
        'meta-gradient': 'var(--bg-gradient)',
      },
      backdropBlur: {
        'xs': '2px',
      }
    },
  },
  plugins: [],
}
