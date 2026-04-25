/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        shell: '#060B16',
        panel: '#0E1729',
        border: '#1A2940',
        accent: '#2DE2B0',
        accentSoft: '#1DAE89'
      },
      boxShadow: {
        card: '0 8px 40px rgba(0, 0, 0, 0.25)',
      },
      backgroundImage: {
        radial: 'radial-gradient(circle at 20% 20%, rgba(45,226,176,0.12), transparent 35%), radial-gradient(circle at 80% 10%, rgba(34,211,238,0.08), transparent 30%)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
