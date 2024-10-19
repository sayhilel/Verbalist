import audioRecorder
import groqCommands

import os

audio_file = os.path.dirname(os.path.abspath(__file__)) + "/Audio/tmp.wav"


def recordTest():
    recorder = audioRecorder.AudioRecorder(output_filename=audio_file)
    recorder.start_recording()
    import time
    time.sleep(5)
    recorder.stop_recording()
    groqCommands.get_command(audio_file)


recordTest()
