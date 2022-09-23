// const colors = require("tailwindcss/colors");

const defaultPreset = {
  variants: {
    extends: {
      backgroundColor: ["disabled"],
      textColor: ["disabled"],
    },
  },
  plugins: [
    require("@tailwindcss/typography"),
    // require("@tailwindcss/forms")({
    //   strategy: "class",
    // }),
    require("daisyui"),
  ],
  daisyui: {
    themes: ["light", "dark"],
  },
};
function contentAll(rootDir = "./jembeui") {
  const content = [
    `${rootDir}/components/**/*.py`,
    `${rootDir}/includes/**/*.py`,
    `${rootDir}/templates/jembeui/components/**/*.html`,
    `${rootDir}/templates/jembeui/jembeui.html`,
    `${rootDir}/templates/jembeui/includes/**/*.html`,
    `${rootDir}/templates/jembeui/macros/**/*.html`,
  ];
  return content;
}
module.exports = {
  defaultPreset,
  contentAll,
};
