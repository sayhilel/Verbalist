import os, sys
from dotenv import load_dotenv
from groq import Groq


load_dotenv()
groq_key = os.environ.get("GROQ_API_KEY")


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_command(filename):
    client = Groq(api_key=groq_key)

    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="distil-whisper-large-v3-en",
            response_format="json",
            language="en",
            temperature=0.0,
        )

    #   eprint(transcription.text)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a VSCode extension that responds with specific editBuilder function calls based on user requests. Your responses should only include valid function calls such as editBuilder.insert, editBuilder.delete, or editBuilder.replace. You can also stitch together multiple commands to fulfill a request. If a valid command exists for the situation, return it in the following format:"
                + '{ "function": ["func1", "func2", "func3"], "args": ["(arg1-1, arg1-2, arg1-3)", "(arg2-1, arg2-2, arg2-3)", "(arg3-1, arg3-2, arg3-3)"]}'
                + "The format includes:"
                + "function: An array of the functions to be called, e.g., delete, insert, or replace."
                + "args: An array of the argument lists for each function, formatted as strings. Each function call has its own arguments, and the number of arguments depends on the specific function."
                + "Use valid function calls only (e.g., editBuilder.delete(location: Range | Selection): void, editBuilder.insert(location: Position, value: string): void, editBuilder.replace(location: Range | Position | Selection, value: string): void). "
                + "Here is a list of the functions:"
                + "delete(location: Range | Selection): void ,"
                + "insert(location: Position, value: string): void, "
                + "replace(location: Range | Position | Selection, value: string): void, "
                + "setEndOfLine(endOfLine: EndOfLine): void"
                + "The Range object is constructed as follows:"
                + "new vscode.Range(start: Position, end: Position): Range"
                + "new vscode.Range(startLine: number, startCharacter: number, endLine: number, endCharacter: number): Range"
                + "For a Range, the ending is excluded, for example, if you want to remove 2 lines, the range would be new Range(someLineY, someLineX, someLineY+2,someLineX)"
                + "A Position object is constructed as follows:"
                + "new vscode.Position(line: number, character: number): Position"
                + "If the command requires the current cursor position, use new vscode.Position(editor.selection.active.line, editor.selection.active.character) to get it. Make sure all necessary arguments are provided to create valid function calls. If no valid command exists, return nothing."
                + "For deletion that spans multiple lines, the range should include the final line as well. For example, to delete 4 lines starting from the current line, the range would look like:"
                + "new vscode.Range(editor.selection.active.line, 0, editor.selection.active.line + 4, 0)"
                + "Remember:"
                + "editor refers to the current editor."
                + "vscode is imported as vscode."
                + "Do not include boilerplate text or comments. If you are unsure, don't output anything.",
            },
            {
                "role": "user",
                "content": f"Return the correct methods and their args for following request:'{transcription.text}'",
            },
        ],
        model="llama3-8b-8192",
        temperature=0.0,
        max_tokens=1024,
        top_p=0.1,
        stop=None,
        stream=False,
    )
    vscode_command = chat_completion.choices[0].message.content
    #   eprint(vscode_command)

    return vscode_command
