import sys
import audioRecorder
import groqCommands
import os

ofile = os.getcwd() + "/audio.wav"
recorder = audioRecorder.AudioRecorder(output_filename=ofile)



def listen_for_commands():
    try:
        while True:
         # Read a line from stdin and strip any whitespace
            command = sys.stdin.readline().strip()
            #eprint(f"Received command: {command}")
        
            # Respond to the "start" command
            if command == "start":
                if not recorder.is_recording:
                    #print("Received 'start' command.")
                    recorder.start_recording()
                    
                    # Delete file
                    continue
                else:
                    #print("Already recording.")
                    pass
        
            # Respond to the "stop" command
            if command == "stop":
                if recorder.is_recording:
                    #print("Received 'stop' command.")
                    recorder.stop_recording()
                    print("COMMAND_START")
                    print(groqCommands.get_command(ofile))
                    print("COMMAND_END")

    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)

listen_for_commands()
