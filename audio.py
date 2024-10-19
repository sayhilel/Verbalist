import sys
import time
import sounddevice as sd
import numpy as np
import wave

class AudioRecorder:
    def __init__(self, samplerate=44100, channels=1, output_filename="output.wav"):
        self.samplerate = samplerate
        self.channels = channels
        self.output_filename = output_filename
        self.frames = []
        self.is_recording = False
        self.stream = None

    def _callback(self, indata, frames, time, status):
        if status:
            print(status, flush=True)
        if self.is_recording:
            self.frames.append(indata.copy())  # 将录音帧保存

    def start_recording(self):
        if not self.is_recording:
            print("Recording started...")
            self.frames = []  # 清空之前的录音数据
            print("Recording started 2...")
            self.is_recording = True
            print("Recording started 3...")
            self.stream = sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=self._callback)
            print("Recording started ##4...")
            self.stream.start()  # 开始录音
            print("Recording started ##5...")
            time.sleep(5)
            self.stream.stop()

    def stop_recording(self):
        if self.is_recording:
            print("Stopping recording...")
            self.is_recording = False
            if self.stream:
                self.stream.stop()  # 停止录音
                self.stream.close()
            self._save_audio()

    def _save_audio(self):
        # 将录制的音频保存为 WAV 文件
        audio_data = np.concatenate(self.frames, axis=0)
        audio_data = (audio_data * 32767).astype(np.int16)  # 将 float32 数据转换为 16-bit PCM 格式

        with wave.open(self.output_filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 每个样本 2 字节 (16 bits)
            wf.setframerate(self.samplerate)
            wf.writeframes(audio_data.tobytes())

        print(f"Recording saved to {self.output_filename}")

recorder = AudioRecorder(output_filename="my_audio.wav")

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