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
                "content": "You are a VScode extention that replies with editor actions depending on what the user requests. You only return the editor action command as a string. Only give me a command if that valid command exists for that situation."
            },
            {
                "role": "user",
                "content": f"Return a VSCode extention API editor action to achieve the following:'{transcription.text}'"
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

