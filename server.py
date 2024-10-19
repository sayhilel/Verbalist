import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_key = os.environ.get("GROQ_API_KEY")


def main():
    client = Groq()
    
    filename = os.path.dirname(__file__) + "/Audio/output_audio.m4a"
    
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
        file=(filename, file.read()),
        model="distil-whisper-large-v3-en", 
        prompt="Specify context or spelling", 
        response_format="json", 
        language="en", 
        temperature=0.0  

    )
    
    print(transcription.text)

if __name__ == "__main__":
    main()
