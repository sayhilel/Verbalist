import sys
import time
import sounddevice as sd
import numpy as np
import wave
import 


def listen_for_commands():
    while True:
        # Read a line from stdin and strip any whitespace
        print("entered loop")
        command = sys.stdin.readline().strip()
        print(f"Received command: {command}")
        
        # Respond to the "start" command
        if command == "start":
            if not recorder.is_recording:
                print("Received 'start' command.")
                recorder.start_recording()
                continue
            else:
                print("Already recording.")
        
        # Respond to the "stop" command
        elif command == "stop":
            if recorder.is_recording:
                print("Received 'stop' command.")
                recorder.stop_recording()
                break  # Exit the loop after stopping
            else:
                print("Not currently recording.")

print("hello from python subprocess!")
listen_for_commands()
