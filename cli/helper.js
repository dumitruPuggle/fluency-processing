const {
  printShortcutCommands,
  repeater,
  space,
} = require("./cli-information.js");
const yaml = require("js-yaml");
const fs = require("fs");

// Get document, or throw exception on error
try {
  const doc = yaml.load(fs.readFileSync("./commands.yaml", "utf8"));
  repeater(2, space);
  printShortcutCommands(doc);
  repeater(2, space);
} catch (e) {
  console.log(e);
}
