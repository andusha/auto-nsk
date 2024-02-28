/** @type {import('tailwindcss').Config} */
const Path = require("path");
const pwd = process.env.PWD;

// We can add current project paths here
const projectPaths = [
  Path.join(pwd, "../templates/**/*.html"),
  Path.join(pwd, "./src/**/*.js"),
  Path.join(pwd, "./node_modules/flowbite/**/*.js"),
];

const contentPaths = [...projectPaths];
console.log(`tailwindcss will scan ${contentPaths}`);

module.exports = {
  content: contentPaths,
  theme: {
    extend: {
      colors: {
        'main': '#ff0000',
      },
      fontFamily: {
        title: 'Open Sans, sans-serif',
        'text-title': 'Inter, sans-serif', 
        text: 'Ubuntu, sans-serif',
      },
      letterSpacing: {
        'title': '0.21rem',
        'main': '0.15rem',
      },
      gridTemplateColumns: {
        'autofit': 'repeat(auto-fit, minmax(33%, 1fr))',
      }
    },
  },
  plugins: [
    require("flowbite/plugin"),
    require('flowbite-typography'),
  ],
};

