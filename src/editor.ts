import * as vscode from "vscode";

//function to run vs code commands
export default function runEditorAction(command: string) {
  // Get the active text editor
  const editor = vscode.window.activeTextEditor;

  if (!editor) {
    vscode.window.showInformationMessage("No active editor found.");
    return;
  }

  const editCommandString =
    "editor.edit((editBuilder) => {\n" + command + "});";
  eval(editCommandString);
  console.log("passed eval");
}
