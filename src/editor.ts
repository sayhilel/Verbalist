import * as vscode from "vscode";
import Doggy from "./doggy"; // Import Doggy class

export default function runEditorAction(
  command: string,
  context: vscode.ExtensionContext
) {
  // Get the active text editor
  const editor = vscode.window.activeTextEditor;

  if (!editor) {
    vscode.window.showInformationMessage("No active editor found.");
    return;
  }

  const doggy = new Doggy(context.extensionUri); // Pass extensionUri to Doggy

  // Show the dog character with the action
  doggy.showDog(`Executing command: ${command}`);

  try {
    const editCommandString =
      "editor.edit((editBuilder) => {\n" + command + "});";
    eval(editCommandString);
    console.log("passed eval");
  } catch (error) {
    vscode.window.showErrorMessage(`Error executing command: ${error}`);
  } finally {
    // Hide the dog character after the action is executed
    doggy.hide();
  }
}
