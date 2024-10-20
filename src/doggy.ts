import * as vscode from "vscode";
import * as path from "path";

export default class Doggy {
  private dogPanel: vscode.WebviewPanel | undefined;
  private extensionUri: vscode.Uri;

  constructor(extensionUri: vscode.Uri) {
    this.extensionUri = extensionUri;
    this.dogPanel = undefined;
  }

  showDog(action: string) {
    if (!this.dogPanel) {
      this.dogPanel = vscode.window.createWebviewPanel(
        "doggy",
        "Cute Doggy",
        vscode.ViewColumn.Two, // Show in the second editor column
        {}
      );
    }

    // Get the local path to the gif using the extensionUri
    const dogGifPath = vscode.Uri.joinPath(
      this.extensionUri,
      "media",
      "doggy.gif"
    );

    const htmlContent = `
      <html>
      <body style="text-align: center;">
        <div style="font-size: 16px;">
          <img src="${this.dogPanel.webview.asWebviewUri(
            dogGifPath
          )}" alt="Cute Doggy" style="width: 150px;"/>
          <p>${action}</p>
        </div>
      </body>
      </html>
    `;

    this.dogPanel.webview.html = htmlContent;
  }

  hide() {
    if (this.dogPanel) {
      this.dogPanel.dispose();
      this.dogPanel = undefined;
    }
  }
}
