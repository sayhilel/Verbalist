import runEditorAction from "./editor";
import * as vscode from "vscode";

// Function to process command output from stdin
function consoleToCommands(commandString: string) {
  console.log("CHECK:", commandString);
  if (commandString === "COMMAND_START") {
    return;
  }
  try {
    // Look for the COMMAND_START and COMMAND_END delimiters
    const commandStart = commandString.indexOf("COMMAND_START");
    const commandEnd = commandString.indexOf("COMMAND_END");

    if (commandStart !== -1 || commandEnd !== -1) {
      // Extract the actual command between the delimiters
      const extractedCommand = commandString
        .slice(0, commandEnd)
        .trim();

      // Run the editor action using the extracted command
      runEditorAction(extractedCommand);
    } else {
      // If the delimiters are not found, show an error
      vscode.window.showErrorMessage(
        "Invalid command: missing COMMAND_START or COMMAND_END."
      );
    }
  } catch (error: any) {
    // Catch any unexpected errors and display them to the user
    vscode.window.showErrorMessage(
      "Error processing command: " + error.message
    );
  }
}

export default consoleToCommands;  
