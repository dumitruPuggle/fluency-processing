import util from "node:util";
import ChildProcess from "node:child_process";

const exec = util.promisify(ChildProcess.exec);

async function installDeps() {
  const installCommands = [
    "npm install -g typescript",
    "npm install -g ts-node",
    "npm i --save-dev @types/node",
    "npm i colors",
    "npm i inquirer",
    "npm i arg",
    "npm i js-yaml",
  ];
  const { stdout, stderr } = await exec(installCommands.join(" && "));
  const installSuccess = stderr.length === 0;
  return {
    installSuccess,
  };
}

import colors from "colors";
import {
  printCLIInformation,
  printShortcutCommands,
  space,
  repeater,
} from "../cli-information.js";

installDeps().then(({ installSuccess }) => {
  if (installSuccess) {
    repeater(4, space);
    printCLIInformation();
    console.log(colors.green("Success! Installation complete."));
    repeater(3, space);
    printShortcutCommands([
      {
        instruction: "To see commands list",
        command: "yarn show-commands",
      },
    ]);
    space();
  }
});
