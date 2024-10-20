import { spawn } from "child_process";
import * as vscode from "vscode";
import * as path from 'path';
import runEditorAction from "./editor";

let recordingProcess: any = null;
export function activate(context: vscode.ExtensionContext) {

  const extensionPath = context.extensionPath;
  const pythonPath = path.join(extensionPath, 'venv', 'bin', 'python3')
  const filePath = path.join(extensionPath, 'backend', 'IPC.py');

  //----------------------------------------------
  // Buffer to accumulate incoming data from stdin
  let buffer = "";

  // Function to process command output from stdin
  function processCommandInput() {
    const commandStart = buffer.indexOf("COMMAND_START");
    const commandEnd = buffer.indexOf("COMMAND_END");

    if (commandStart !== -1 && commandEnd !== -1) {
      // Extract command between the delimiters
      const commandString = buffer
        .slice(commandStart + "COMMAND_START".length, commandEnd)
        .trim()
        .replace("\n", "");

      // Call runEditorAction with the extracted command
      if (commandString) {
        runEditorAction(commandString);
      }

      // Remove the processed command from the buffer
      buffer = buffer.slice(commandEnd + "COMMAND_END".length);

    }
  }

  //-----------------------------------------------
  context.subscriptions.push(
    vscode.commands.registerCommand("verbalist.captureAudio", () => {
      const cmd = pythonPath;
      const args = ['-u', filePath];


      if (!recordingProcess) {
        recordingProcess = spawn(cmd, args);
      }
      recordingProcess.stdout.on("data", (data: any) => {
        console.log(`${data}`);
        buffer += data;
        processCommandInput()
      });
      recordingProcess.stderr.on("data", (data: any) => {
        console.log(`STDERR:${data}`);
      });
      vscode.window.showInformationMessage("spawned recording process");
      recordingProcess.stdin.write("start" + "\n");
      vscode.window.showInformationMessage("started recording process!");

      return recordingProcess;
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("verbalist.stopAudio", () => {
      if (recordingProcess) {
        vscode.window.showInformationMessage("stopping recording process!");
        recordingProcess.stdin.write("stop\n");
        recordingProcess.on("exit", () => {
          recordingProcess = null;
        });
      } else {
        vscode.window.showInformationMessage("no recording process to kill");
      }
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("verbalist.runCommand", () => {
    })

  );


}

export function deactivate() { }
