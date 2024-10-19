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
            self.is_recording = True
            self.stream = sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=self._callback)
            self.stream.start()  # 开始录音

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


