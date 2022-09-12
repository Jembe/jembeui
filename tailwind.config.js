const { defaultPreset, contentAll } = require("./jembeui/src/css/tailwind.config.js");

module.exports = {
  content: [...contentAll()],
  presets: [defaultPreset],
};
