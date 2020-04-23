module.exports = {
  important: true,
  theme: {
    fontFamily: {
      sans: ["Myniad", "sans-serif"],
    },
    extend: {
      screens: {
        'xxl': '1440px',
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
        "red-500": "#c41737",
      },
      maxWidth: {
        "7xl": "80rem"
      },
      spacing: {
        "1_5": "0.375rem",
        "36": "9rem",
        "14": "3.5rem",
        "18": "4.5rem",
        "1000": "1000px",
        "500": "500px",
        "400": "400px",
        "320": "320px",
      },
    }
  },
  variants: {
    boxShadow: ["responsive", "hover", "focus", "focus-within", "group-hover"],
    textColor: ["responsive", "hover", "focus", "group-hover", "focus-within"],
    borderColor: ["responsive", "hover", "group-hover", "focus"],
    scale: ["responsive", "hover", "focus", "active", "group-hover"],
    opacity: ['responsive', 'hover', 'focus', "group-hover"],
    width: ["responsive", "hover", "focus", "focus-within", "group-hover"],
  },
  corePlugins: {
    container: false,
  }
};
