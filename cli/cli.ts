const util = require("node:util");
const ChildProcess = require("node:child_process");

const exec = util.promisify(ChildProcess.exec);

const startFlaskApp = async () => {
  const startCommands = ["cd ..", `source "venv/bin/activate"`, "flask run"];
  const end = await exec(startCommands.join(" && "));
  try {
    console.log(end);
  } catch (e) {
    console.log(e);
  }
};

function startApp() {
  startFlaskApp();
}

startApp();
