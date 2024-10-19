import os, sys
from dotenv import load_dotenv
from groq import Groq


load_dotenv()
groq_key = os.environ.get("GROQ_API_KEY")

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_command(filename):
    client = Groq()
    
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
        file=(filename, file.read()),
        model="distil-whisper-large-v3-en", 
        response_format="json", 
        language="en", 
        temperature=0.0  

    )
    
    print(transcription.text)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"You are a translator from natural language to VScode  vscode.editor API. Only reply with  vscode.editor to achieve the required effect as stated by '{transcription.text}'"
            },
            {
                "role": "user",
                "content": "```json"
            }
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )
    vscode_command = chat_completion.choices[0].message.content
    print(vscode_command)  

