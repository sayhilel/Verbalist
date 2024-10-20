import * as vscode from "vscode";

export function searchAndEditWithRegex(
  regex: RegExp,  // Accepts a regular expression
  editCallback: (editBuilder: vscode.TextEditorEdit, range: vscode.Range) => void  // Callback for handling edit operations
) {
  // Get the active text editor
  const editor = vscode.window.activeTextEditor;

  if (editor) {
    const document = editor.document;
    const text = document.getText(); // Get the entire text of the document

    let match;
    const rangesToEdit: vscode.Range[] = [];

    // Iterate over all matches of the regular expression
    while ((match = regex.exec(text)) !== null) {
      // Get the start and end positions of the match
      const startPos = document.positionAt(match.index);
      const endPos = document.positionAt(match.index + match[0].length);

      // Create the range to be edited (deleted or replaced)
      rangesToEdit.push(new vscode.Range(startPos, endPos));
    }

    // Perform edit operations using the provided callback
    editor.edit(editBuilder => {
      // Process the ranges in reverse order to avoid affecting the subsequent ranges
      for (let i = rangesToEdit.length - 1; i >= 0; i--) {
        editCallback(editBuilder, rangesToEdit[i]);  // Invoke the callback for each range
      }
    }).then(success => {
      if (success) {
        console.log(`All matches for regex ${regex} have been processed.`);
      } else {
        console.error('Failed to process the matches.');
      }
    });
  } else {
    console.log('No active editor found.');
  }
}

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

  try {
    eval(editCommandString);
    console.log("passed eval");

  } catch (e) {
    console.error(e);
  }

}

