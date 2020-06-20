module.exports = {
  important: true,
  theme: {
    fontFamily: {
      sans: ["Myniad", "sans-serif"],
    },
    animations: {
      "translate-x-3": {
        "0%": {
          transform: "translateX(0)"
        },
        "50%": {
          transform: "translateX(0.75rem)"
        },
        "100%": {
          transform: "translateX(0)"
        }
      }
    },
    extend: {
      screens: {
        "xxl": "1440px",
      },
      borderWidth: {
        "5": "5px",
      },
      borderRadius: {
        md: "6px"
      },
      boxShadow: {
        "outline-error": "0 0 0 3px rgba(194, 48, 48, 0.5);"
      },
      colors: {
        "purple": "#7F006B",
        green: {
          50: "#fcfefb",
          100: "#f6fff1",
          200: "#d8f2d8",
          300: "#aee1a5",
          400: "#81c155",
          500: "#3a9d00",
          600: "#308701",
          700: "#2b7b03",
          800: "#236707",
          900: "#1a4614"
        },
        "white-75": "rgba(255, 255, 255, 0.75)",
        "black-75": "rgba(0, 0, 0, 0.75)",
        "black-90": "rgba(0, 0, 0, 0.9)",
        "brown": "#644327",
        "gray-50": "#fafafa",
        "gray-150": "#f7f7f7",
        "red-500": "#c41737",
      },
      maxWidth: {
        "7xl": "80rem"
      },
      maxHeight: {
        "0": "0",
        "1000": "1000px"
      },
      spacing: {
        "1_5": "0.375rem",
        "7": "1.75rem",
        "9": "2.25rem",
        "36": "9rem",
        "14": "3.5rem",
        "18": "4.5rem",
        "700": "700px",
        "1000": "1000px",
        "1100": "1100px",
        "1200": "1200px",
        "500": "500px",
        "400": "400px",
        "320": "320px",
        "1/2-screen": "50vh",
      },
      cursor: {
        "zoom-in": "zoom-in",
      }
    }
  },
  variants: {
    boxShadow: ["responsive", "hover", "focus", "focus-within", "group-hover"],
    backgroundColor: ["responsive", "hover", "focus", "focus-within", "group-hover"],
    textColor: ["responsive", "hover", "focus", "group-hover", "focus-within"],
    borderColor: ["responsive", "hover", "group-hover", "focus"],
    scale: ["responsive", "hover", "focus", "active", "group-hover"],
    opacity: ["responsive", "hover", "focus", "group-hover"],
    width: ["responsive", "hover", "focus", "focus-within", "group-hover"],
    animations: ["responsive", "group-hover", "hover"],
    placeholderColor: ["responsive", "focus", "hover", "active"],
    fontWeight: ["responsive", "hover", "focus", "active", "group-hover"],
    translate: ["responsive", "hover", "focus", "active", "group-hover"],
    rotate: ["responsive", "hover", "focus", "active", "group-hover"],
    textDecoration: ["responsive", "hover", "focus", "active", "group-hover"],
    display: ["responsive", "hover", "focus", "active", "group-hover", "group-focus"],
  },
  corePlugins: {
    container: false,
  },
  plugins: [
    require("tailwindcss-animations"),
    require("tailwindcss-animatecss")({
      classes: []
    }),
  ]
};
