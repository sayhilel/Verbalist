import { spawn } from "child_process";
import * as vscode from "vscode";
import * as path from 'path';
import consoleToCommands from "./parser";

let recordingProcess: any = null;
export function activate(context: vscode.ExtensionContext) {

  const extensionPath = context.extensionPath;
  const pythonPath = path.join(extensionPath, 'venv', 'bin', 'python3')
  const filePath = path.join(extensionPath, 'backend', 'IPC.py');

  context.subscriptions.push(
    vscode.commands.registerCommand("verbalist.captureAudio", () => {
      const cmd = pythonPath;
      const args = ['-u', filePath];


      if (!recordingProcess) {
        recordingProcess = spawn(cmd, args);
      }
      recordingProcess.stdout.on("data", (data: any) => {
        console.log(`${data}`)
        consoleToCommands(`${data}`)

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
          recordingProcess.stdout.on("data", (data: any) => {
            console.log(`${data}`)
            consoleToCommands(`${data}`)

          });
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
