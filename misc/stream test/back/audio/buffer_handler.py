import wave
import numpy as np


class BufferHanlder:
    def __init__(self, id: str, thresh: float):
        self.id: str = id
        self.counter: int = 0
        self.thresh: float = thresh
        self.buffer: list[np.ndarray] = []
        self.was_speaking: bool = False

    def handle_audio_data(self, audio_data: bytes) -> bool:
        samples = self.binary_to_nparray(audio_data)
        max_sample = np.max(np.abs(samples))
        is_speaking = max_sample > self.thresh
        was_speaking = self.was_speaking
        self.was_speaking = is_speaking
        self.buffer.append(samples)
        if not is_speaking and was_speaking:
            self.save_audio_to_wav()
        return (is_speaking, was_speaking, max_sample)

    def save_audio_to_wav(self):

        if len(self.buffer) < 1:
            print("BufferHandler with id", self.id, "did not receive any data")
            return

        audio_data_combined = np.concatenate(self.buffer)

        # audio_data_combined.tobytes() pipe these directly (clear buffer first to allow new data)

        file_name = f"./saved/{self.id}_{self.counter}.wav"
        with wave.open(file_name, "wb") as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(48000)  # Sample rate
            wf.writeframes(audio_data_combined.tobytes())
        self.counter += 1
        self.buffer.clear()

    @staticmethod
    def binary_to_nparray(binary_data: bytes):
        return np.frombuffer(binary_data, dtype=np.int16)
