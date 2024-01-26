/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'primary': '#09090b',
        'secondary': '#fafafa',
        'tertiary': '#272A29',
        'tertiary-text': '#838383'
      },
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
      },
      minWidth: {
        'table': '550px',
      },
    },
  },
  plugins: [],
}

