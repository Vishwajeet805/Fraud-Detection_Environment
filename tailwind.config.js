/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        base: '#060a12',
        surface: '#0b1220',
        panel: '#101a2b',
        accent: '#1dd4bf',
        alert: '#ef4444',
        caution: '#f59e0b',
      },
      boxShadow: {
        soft: '0 10px 30px rgba(0, 0, 0, 0.25)',
      },
      backgroundImage: {
        'mesh-soft':
          'radial-gradient(circle at 20% 20%, rgba(29, 212, 191, 0.10), transparent 40%), radial-gradient(circle at 80% 10%, rgba(56, 189, 248, 0.10), transparent 35%), radial-gradient(circle at 50% 80%, rgba(16, 185, 129, 0.08), transparent 40%)',
      },
    },
  },
  plugins: [],
}
