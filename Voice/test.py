import audioRecorder
import groqCommands

import os

audio_file = os.path.dirname(os.path.abspath(__file__)) + "/Audio/tmp.wav"
audioRecordHandler=audioRecorder.AudioRecorder(output_filename=audio_file)

audioRecorder.recordTest()
groqCommands.get_command(audio_file)

