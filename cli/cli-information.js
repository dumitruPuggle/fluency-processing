import colors from "colors";

const space = () => {
  console.log("");
};

const repeater = (iterations, func) => {
  for (let i = 0; i < iterations; i++) {
    func();
  }
};

const printCLIInformation = () => {
  space();
  console.log(colors.bold("ℹ️ Fluency CLI Processing Api (v 1.0) #0001"));
  console.log(
    colors.gray(
      "This software is protected by copyright law and international treaties. \nUnauthorized reproduction or distribution of this software, or any porti\non of it, may result in severe civil and criminal penalties, and will be\nprosecuted to the maximum extent possible under law."
    )
  );
  space();
};

const printShortcutCommands = (shortcuts) => {
  console.log(colors.bold("CLI commands used for backend:"));
  space();
  shortcuts.forEach((shortcut) => {
    console.log(
      `${colors.italic.dim(shortcut.instruction)}:`,
      colors.yellow(shortcut.command)
    );
  });
};

export { printCLIInformation, printShortcutCommands, space, repeater };
