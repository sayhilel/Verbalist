const { spawn } = require("child_process");
import * as vscode from "vscode";

let recordingProcess: any = null;
const pythonPath = "/home/ecs_032c/code/Verbalist/venv/bin/python3";
const filePath = "/home/ecs_032c/code/Verbalist/audio.py";
export function activate(context: vscode.ExtensionContext) {
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
}

// This method is called when your extension is deactivated
export function deactivate() {}
