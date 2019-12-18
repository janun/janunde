module.exports = {
  important: true,
  theme: {
    fontFamily: {
      sans: ["Cabin", "sans-serif"],
      serif: ["Crimson Text", "serif"]
    },
    extend: {
      borderRadius: {
        md: "6px"
      },
      boxShadow: {
        "outline-error": "0 0 0 3px rgba(194, 48, 48, 0.5);"
      },
      colors: {
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
        "white-75": "rgba(255, 255, 255, 0.75)"
      },
      maxWidth: {
        "7xl": "80rem"
      },
      spacing: {
        "1.5": "0.375rem",
        "36": "9rem"
      },
    }
  },
  variants: {
    boxShadow: ["responsive", "hover", "focus", "focus-within"],
    textColor: ["responsive", "hover", "focus", "group-hover", "focus-within"],
    borderColor: ["responsive", "hover", "focus"],
  },
  corePlugins: {
    container: false,
  }
};
