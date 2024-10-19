import os
import wave
import sounddevice as sd
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_key = os.environ.get("GROQ_API_KEY")

SAMPLE_RATE = 44100
DURATION = 5


def record_audio(filename: str, duration: int, sample_rate: int):
    print("Recording started...")
    
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait() 
    print("Recording finished.")

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)  
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())


def get_command(filename):
    client = Groq()
    
    filename = os.path.dirname(__file__) + "/Audio/output_audio.wav"
    
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
                "content": "You are an assistant that helps generate VSCODE editor actions from VSCode api from user instructions. Only reply with the editor commands."
            },
            {
                "role": "user",
                "content": f"Convert this speech into a VSCODE command: '{transcription.text}'"
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
    print("VSCODE Command:", vscode_command)


def main():
    filename = os.path.dirname(__file__) + "/Audio/output_audio.wav"
    record_audio(filename, DURATION, SAMPLE_RATE)
    get_command(filename)

if __name__ == "__main__":
    main()
