import { spawn } from "child_process";
import * as vscode from "vscode";
import * as path from 'path';
import runEditorAction from "./editor";

let recordingProcess: any = null;
export function activate(context: vscode.ExtensionContext) {

  const extensionPath = context.extensionPath;
  const pythonPath = path.join(extensionPath, 'venv', 'bin', 'python3')
  const filePath = path.join(extensionPath, 'backend', 'IPC.py');

  console.log(filePath)
  context.subscriptions.push(
    vscode.commands.registerCommand("verbalist.captureAudio", () => {
      const cmd = pythonPath;
      const args = [filePath];
      console.log("good mroning");

      recordingProcess = spawn(cmd, args);
      recordingProcess.stdout.on("data", (data: any) => {
        console.log(`stdout from python: ${data}`);
      });
      recordingProcess.stderr.on("data", (data: any) => {
        console.log(`STDERR from python: ${data}`);
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
        recordingProcess.kill("SIGINT");
        recordingProcess.on("exit", () => {
          recordingProcess = null;
        });
      } else {
        vscode.window.showInformationMessage("no recording process to kill");
      }
    })
  );
  //   context.subscriptions.push(disposable);
  context.subscriptions.push(
    vscode.commands.registerCommand("verbalist.runCommand", () => {
      runEditorAction("editor.action.deleteLines");
    })
  );
}

// This method is called when your extension is deactivated
export function deactivate() { }
