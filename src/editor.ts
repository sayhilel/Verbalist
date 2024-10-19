import * as vscode from "vscode";

//function to run vs code commands
export default function runEditorAction(command: string) {
  // Get the active text editor
  const editor = vscode.window.activeTextEditor;

  if (!editor) {
    vscode.window.showInformationMessage("No active editor found.");
    return;
  }

  // Execute the command at the current cursor position
  vscode.commands.executeCommand(command).then(() => {
    console.log(`Successfully executed command: ${command}`);
  });
}
