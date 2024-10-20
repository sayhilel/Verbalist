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
    console.log("about to eval, preparing: ");
    // const editCommandString =
    //   "editor.edit((editBuilder) => {\n" + command + "});";
    console.log(command);
    const command_json = JSON.parse(command);
    console.log(command_json);
    const editBuilderFunctionsString = command_json["function"]
      .map(
        (func: any, idx: any) =>
          "editBuilder." + func + command_json["args"][idx]
      )
      .join("");
    console.log("editBuilderFunctionsString: ", editBuilderFunctionsString);
    const editCommandString =
      "editor.edit((editBuilder) => {\n" + editBuilderFunctionsString + "\n});";
    console.log("WILLE VAL: ");
    console.log(editCommandString);
    eval(editCommandString);
    // editor.edit((editBuilder: any) => {
    //   command_json["function"].forEach((func: any, idx: any) => {
    //     console.log("idx, ", ...command_json["args"].map(eval));
    //     // editBuilder[func](
    //     //   new vscode.Range(
    //     //     editor.selection.active.line,
    //     //     0,
    //     //     editor.selection.active.line + 2,
    //     //     0
    //     //   )
    //     // );
    //     editBuilder[func](...command_json["args"].map(eval));
    //   });
    // });
    // console.log(editCommandString);
    // eval(editCommandString);
    console.log("passed eval");
  } catch (error) {
    vscode.window.showErrorMessage(`Error executing command: ${error}`);
  } finally {
    // Hide the dog character after the action is executed
    doggy.hide();
  }
}
