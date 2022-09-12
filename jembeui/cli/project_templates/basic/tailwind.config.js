// const colors = require("tailwindcss/colors");
const { jembeUiDir } = require("./jembeui.config");
const { defaultPreset, contentAll } = require(jembeUiDir +
  "/src/css/tailwind.config.js");

function getJembeUIContent() {
  if (process.env.NODE_ENV === "production") {
    // load list of jembeUi templates used by application
    const { spawnSync } = require("child_process");
    const raw = spawnSync("flask", ["create-tw-content"]);
    return JSON.parse(raw.stdout.toString());
  } else {
    // load all templates from jembeUI
    return contentAll(jembeUiDir);
  }
}

module.exports = {
  presets: [defaultPreset],
  content: [
    ...getJembeUIContent(),
    "./{{ project_name }}/templates/**/*.html",
    "./{{ project_name }}/src/**/*.js",
    "./{{ project_name }}/pages/**/*.py",
    "./{{ project_name }}/components/**/*.py",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
