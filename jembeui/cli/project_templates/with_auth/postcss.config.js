const { jembeUiDir } = require("./jembeui.config");
module.exports = {
  plugins: {
    "postcss-import": {
      resolve: (id) =>
        id.replace(/^JembeUI/, jembeUiDir + "/src/css"),
    },
    tailwindcss: { config: "./tailwind.config.js" },
    autoprefixer: {},
    ...(process.env.NODE_ENV === "production" ? { cssnano: {} } : {}),
  },
};