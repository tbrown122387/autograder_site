const colors = require("tailwindcss/colors");

module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    listStyleType: {
      square: "square",
      roman: "upper-roman",
    },
    colors: {
      transparent: "transparent",
      current: "currentColor",
      black: colors.black,
      white: colors.white,
      gray: colors.gray,
      blue: colors.blue,
      green: colors.emerald,
      orange: colors.orange,
      red: colors.red,
    },
  },
  variants: {
    extend: {
      transitionDuration: ["hover", "focus", "active"],
      transitionTimingFunction: ["hover", "focus"],
      backgroundColor: ["active"],
      ringWidth: ["hover"],
      ringColor: ["hover"],
      ringOffsetWidth: ["hover"],
      ringOffsetColor: ["hover"],
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
