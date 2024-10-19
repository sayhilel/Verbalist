import vscode
from vscode import InfoMessage
import os
import audioRecorder
from groq import Groq

client = Groq(
    api_key="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"
)


ext = vscode.Extension(name="verbalist")

current_file_directory = os.path.dirname(os.path.abspath(__file__))
audioRecordHandler=audioRecorder.AudioRecorder(output_filename=current_file_directory+"/tmp.wav")


@ext.event
async def on_activate():
    vscode.log(f"The Extension '{ext.name}' has started")

@ext.command()
async def hello_world(ctx):

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models in three lines",
        }
    ],
    model="llama3-8b-8192",
    )

    #careful when using this function, you can't have '\n' in the string or else in the extension.js they will throw out a syntaxError
    await ctx.show(InfoMessage(chat_completion.choices[0].message.content))
    return 0


# basic command to start recording audio
@ext.command()
async def startRecordAudio(ctx):
    audioRecordHandler.start_recording()
# basic command to stop recording audio
@ext.command()
async def stopRecordAudio(ctx):
    audioRecordHandler.stop_recording()


ext.run()