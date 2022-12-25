import { printShortcutCommands, repeater, space } from "./cli-information.js";
import yaml from "js-yaml";
import fs from "fs";

// Get document, or throw exception on error
try {
  const doc = yaml.load(fs.readFileSync("./commands.yaml", "utf8"));
  repeater(2, space);
  printShortcutCommands(doc);
  repeater(2, space);
} catch (e) {
  console.log(e);
}
