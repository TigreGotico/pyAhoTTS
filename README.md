# AhoTTS Python

[AhoTTS](https://github.com/aholab/AhoTTS) is a Text-to-Speech conversor for Basque and Spanish. 
It includes linguistic processing and built voices for the languages aforementioned. Its acoustic
engine is based on hts_engine and it uses a high quality vocoder called
AhoCoder. Developed by Aholab Signal Processing Laboratory, at the Bilbao
School of Engineering (University of the Basque Country).

## Install

```bash
git clone https://github.com/TigreGotico/pyAhoTTS
cd AhoTTS
mkdir build
cd build
cmake .. 
make
```

## Usage

not yet packaged, example from `pyahotts.py`
```python
import ctypes
import wave

import numpy as np


class AhoTTS:
    def __init__(self, lib_path: str, data_path: str):
        self.data_path = data_path.encode("utf-8")
        self._load_library(lib_path)
        self.tts = self.lib.create_tts(self.data_path)
        if not self.tts:
            raise RuntimeError("Failed to create TTS instance")

    def _load_library(self, lib_path: str):
        self.lib = ctypes.cdll.LoadLibrary(lib_path)

        self.lib.create_tts.argtypes = [ctypes.c_char_p]
        self.lib.create_tts.restype = ctypes.c_void_p

        self.lib.synthesize_text.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.POINTER(ctypes.c_short)),
            ctypes.POINTER(ctypes.c_int),
        ]
        self.lib.synthesize_text.restype = ctypes.c_int

        self.lib.free_samples.argtypes = [ctypes.POINTER(ctypes.c_short)]
        self.lib.destroy_tts.argtypes = [ctypes.c_void_p]

    def get_tts(self, text: str, lang: str = "eu", wav_path: str = None) -> bytes:
        text_bytes = text.encode("utf-8")
        lang_bytes = lang.encode("utf-8")
        samples_ptr = ctypes.POINTER(ctypes.c_short)()
        length = ctypes.c_int()

        success = self.lib.synthesize_text(
            self.tts, text_bytes, self.data_path,
            ctypes.byref(samples_ptr), ctypes.byref(length)
        )

        if not success or length.value <= 0:
            return b""

        # Convert to NumPy array
        samples_np = np.ctypeslib.as_array(samples_ptr, shape=(length.value,))
        samples_bytes = samples_np.astype(np.int16).tobytes()

        if wav_path:
            with wave.open(wav_path, "wb") as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 2 bytes per sample (16-bit)
                wf.setframerate(16000)  # Assuming 16kHz
                wf.writeframes(samples_bytes)

        self.lib.free_samples(samples_ptr)
        return samples_bytes

    def __del__(self):
        if hasattr(self, 'tts') and self.tts:
            self.lib.destroy_tts(self.tts)
            self.tts = None


if __name__ == "__main__":
    tts = AhoTTS(
        lib_path="/home/miro/PycharmProjects/AhoTTS/build/src/libhtts.so",
        data_path="/home/miro/PycharmProjects/AhoTTS/data_tts"
    )

    audio_bytes = tts.get_tts("Kaixo, Mundua!", lang="eu", wav_path="output.wav")

    if audio_bytes:
        print(f"Generated {len(audio_bytes)} bytes of audio.")
```

## LICENSE

Read `COPYRIGHT_and_LICENSE_code.txt` and `COPYRIGHT_and_LICENSE_voices.txt`

## Credits

> Based on the [fork from @ekaitz-zarraga](https://github.com/ekaitz-zarraga/AhoTTS)
