import sys
import audioRecorder
import groqCommands
import os

ofile = os.getcwd() + "/audio.wav"
recorder = audioRecorder.AudioRecorder(output_filename=ofile)

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
                # delete file
                continue
            else:
                print("Already recording.")
        
        # Respond to the "stop" command
        elif command == "stop":
            if recorder.is_recording:
                print("Received 'stop' command.")
                recorder.stop_recording()
                print(groqCommands.get_command(ofile))
                break  # Exit the loop after stopping
            else:
                print("Not currently recording.")

listen_for_commands()
