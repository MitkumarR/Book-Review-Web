/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // For Django templates
    './src/**/*.{js,jsx,ts,tsx}', // For React/JS
    './public/**/*.html', // For public HTML files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

