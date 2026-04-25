/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        base: '#04070f',
        surface: '#0a1020',
        panel: '#0d1528',
        accent: '#29d3ff',
        accentSoft: '#7c8cff',
        danger: '#ff5f7d',
        warning: '#ffb86b',
      },
      boxShadow: {
        soft: '0 20px 60px rgba(3, 7, 18, 0.52)',
        glow: '0 0 0 1px rgba(41, 211, 255, 0.22), 0 30px 50px rgba(9, 26, 58, 0.5)',
      },
      backgroundImage: {
        'mesh-soft':
          'radial-gradient(circle at 20% 15%, rgba(41, 211, 255, 0.08), transparent 32%), radial-gradient(circle at 82% 2%, rgba(124, 140, 255, 0.08), transparent 28%), radial-gradient(circle at 50% 84%, rgba(71, 85, 172, 0.08), transparent 34%)',
      },
    },
  },
  plugins: [],
}
