/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#101828",
        brand: {
          50: "#eef4ff",
          100: "#e0eaff",
          500: "#6172f3",
          600: "#444ce7",
          700: "#3538cd"
        }
      },
      boxShadow: {
        card: "0 1px 2px rgba(16, 24, 40, 0.05)"
      }
    }
  },
  plugins: []
};
