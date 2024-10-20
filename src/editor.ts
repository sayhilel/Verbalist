import * as vscode from "vscode";

//function to run vs code commands
export default function runEditorAction(command: string) {
  // Get the active text editor
  const editor = vscode.window.activeTextEditor;
  command = command.trim();

  if (!editor) {
    vscode.window.showInformationMessage("No active editor found.");
    return;
  }
  // Execute the command at the current cursor position
  const actualCommand =
    "(textEditor, edit) => {\n" +
    "textEditor.edit((editBuilder) => {\n" +
    command +
    "})};";
  const registerCommandString =
    'vscode.commands.registerTextEditorCommand("verbalist.RUN_COMMAND",' +
    actualCommand +
    ");";
  eval(registerCommandString);
  vscode.commands.executeCommand("verbalist.RUN_COMMAND").then(
    () => {
      console.log(`Successfully executed command: ${command}`);
    },
    (error) => {
      vscode.window.showErrorMessage(
        `Failed to execute command: ${command}. Error: ${error}`
      );
    }
  );
}
