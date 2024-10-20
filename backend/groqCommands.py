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
        temperature=0.0  

    )
    
    eprint(transcription.text)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a VSCode extension that responds with specific editor builder function calls based on user requests. Your responses should only include valid function calls such as editBuilder.insert, editBuilder.delete, or editBuilder.replace. You can also stitch together multiple commands to fulfill a request. If a valid command exists for the situation, return it as a string. Otherwise, return ERR. The API includes the following methods:delete(location: Range | Selection): void ,insert(location: Position, value: string): void, replace(location: Range | Position | Selection, value: string): void, setEndOfLine(endOfLine: EndOfLine): void, The Range object is constructed as follows: new Range(start: Position, end: Position): Range new Range(startLine: number, startCharacter: number, endLine: number, endCharacter: number): Range A range is defined by an ordered pair of two positions and is guaranteed that start.isBeforeOrEqual(end). The position is constructed as follows:new Position(line: number, character: number): Position. Make sure to provide all necessary arguments in your responses to create valid function calls. If you need current cursor position use the expression: new vscode.Position(editor.selection.active.line, editor.selection.active.character) to get the cursor, use this in your reply if needed; DO NOT REPLY WITH NON CODE BOILER PLATE. If you are unsure don't do anything" 
            },
            {
                "role": "user",
                "content": f"Return a VSCode edit.Builder function call with correct params to achieve the following:'{transcription.text}'"
            }
        ],
        model="llama3-8b-8192",
        temperature=0.0,
        max_tokens=1024,
        top_p=0.1,
        stop=None,
        stream=False,
    )
    vscode_command = chat_completion.choices[0].message.content
    eprint(vscode_command)

    return vscode_command

