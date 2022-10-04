// Prints version of this/current package from setup.cfg
// used by scripts in package.json
var fs = require("fs"),
  ini = require("ini");

let config = ini.parse(fs.readFileSync("./setup.cfg", "utf-8"));
console.log(config.metadata.version)