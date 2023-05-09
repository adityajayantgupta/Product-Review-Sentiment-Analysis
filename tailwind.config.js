/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
    screens:{
      'sm': {'max': '700px'},
      'md': '701px',
      'lg': '800px',
    },
  },
  plugins: [],
}