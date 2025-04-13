/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{html,js,svelte,ts}', // Scan all relevant files
  ],
  theme: {
    extend: {
      colors: {
        'dark': '#020013',
        'purple': {
          '950': '#0a041d',
          '900': '#12082f',
          '800': '#1e0f4d',
          '700': '#2a156b',
          '600': '#3d25a0',
          '500': '#4e30cc',
          '400': '#6f55e4',
          '300': '#9583ed',
          '200': '#bcb3f5',
          '100': '#e3defa',
        },
        'neon': {
          'pink': '#ff2cc4',
          'purple': '#a742ff',
          'blue': '#2f8fff',
          'green': '#00ff99',
          'red': '#ff4500',
        }
      },
      backgroundImage: {
        'purple-gradient': 'radial-gradient(circle at top, rgba(87, 13, 248, 0.5) 0%, rgba(18, 8, 47, 0) 50%)',
      },
      backdropBlur: {
        'xs': '2px',
      },
    },
  },
  plugins: [],
};
