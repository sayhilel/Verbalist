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
    
 #   eprint(transcription.text)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a single task unit designed to generate a JSON in the following format: " +
                    "{ \"function\": [\"func1\", \"func2\", \"func3\"], \"args\": [\"(arg1-1, arg1-2, arg1-3)\", \"(arg2-1, arg2-2, arg2-3)\", \"(arg3-1, arg3-2, arg3-3)\"] }" + "There can be from 0 to n args for any func" +
                    "You will process the user request and using one or more of the following function combinations complete the user request" +
                    "delete(location: Range | Selection): void" +
                    "insert(location: Position, value: string): void" +
                    "replace(location: Range | Position | Selection, value: string): void" +
                    "setEndOfLine(endOfLine: EndOfLine): void" +
                    "To constuct the range and position args use the following:" +
                    "new Range(start: Position, end: Position): Range #This range is not end inclusive for example to delete 4 lines range will be: (0, textEditor.selection.active.line + 4)" +
                    "new Position(line: number, character: number): Position." +
                    "Use new Position(line: number, character: number): Position." +
                    "Finally, vscode is imported as vscode AND ONLY REPLY WITH JSON"


            },
            {
                "role": "user",
                "content": f"Return the correct methods and their args for following request:'{transcription.text}'"
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
 #   eprint(vscode_command)
    
    

    return vscode_command

