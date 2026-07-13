/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0B1220",
        brand: {
          25: "#f6f8ff",
          50: "#eef4ff",
          100: "#e0eaff",
          200: "#c7d7fe",
          500: "#6172f3",
          600: "#444ce7",
          700: "#3538cd",
          900: "#1d236f"
        },
        electric: {
          400: "#38bdf8",
          500: "#0ea5e9"
        }
      },
      boxShadow: {
        card: "0 18px 55px rgba(15, 23, 42, 0.08)",
        glow: "0 24px 90px rgba(68, 76, 231, 0.22)",
        soft: "0 12px 35px rgba(15, 23, 42, 0.10)"
      },
      fontFamily: {
        sans: ["Inter", "Fira Sans", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["Fira Code", "ui-monospace", "SFMono-Regular", "monospace"]
      },
      borderRadius: {
        "2xl": "1.25rem",
        "3xl": "1.75rem"
      }
    }
  },
  plugins: []
};
