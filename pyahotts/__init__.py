import ctypes
import platform
import wave
from os.path import dirname, isfile
from typing import Optional

import numpy as np


# AhoTTS SAMPA -> IPA. Matches the mapping shipped with the Aholab phonemizer
# (https://huggingface.co/spaces/arrandi/phonemizer-eus-esp). Used by
# AhoTTS.get_phonemes(ipa=True).
SAMPA_TO_IPA = {
    "p": "p", "b": "b", "t": "t", "c": "c", "d": "d", "k": "k", "g": "ɡ",
    "tS": "tʃ", "ts": "ts", "ts`": "tʂ", "gj": "ɟ", "jj": "ʝ", "f": "f",
    "B": "β", "T": "θ", "D": "ð", "s": "s", "s`": "ʂ", "S": "ʃ", "x": "x",
    "G": "ɣ", "m": "m", "n": "n", "J": "ɲ", "l": "l", "L": "ʎ", "r": "ɾ",
    "rr": "r", "j": "j", "w": "w", "i": "i", "e": "e", "a": "a", "o": "o",
    "u": "u", "y": "y", "Z": "ʒ", "h": "h", "ph": "pʰ", "kh": "kʰ", "th": "tʰ",
}


class AhoTTS:
    """
    A class to interact with AhoTTS, a text-to-speech (TTS) system that uses a shared library for synthesis.

    Attributes:
        data_path (bytes): Path to the directory containing TTS data.
        tts (ctypes.c_void_p): The TTS instance created by the shared library.
        current_lang (Optional[str]): The current language used by the TTS instance.
    """

    # Output sample rate of the bundled voices (Hz). The shipped HTS voices are
    # 16 kHz; the synthesis path emits 16-bit mono PCM at this rate.
    SAMPLE_RATE = 16000

    def __init__(self, lib_path: Optional[str] = None,
                 data_path: str = f"{dirname(__file__)}/data_tts"):
        """
        Initializes the AhoTTS instance, loading the shared library and setting the data path.

        Args:
            lib_path (Optional[str]): Path to the shared library (.so, .dll, .dylib). If None, the library is
                                       determined based on the platform.
            data_path (str): Path to the directory containing TTS data (default is `./data_tts`).
        """
        if lib_path is None:
            lib_path = f"{dirname(__file__)}/libhtts_{platform.machine()}.so"
            if not isfile(lib_path):
                raise FileNotFoundError(f"Please compile and pass the shared library via 'lib_path' argument")

        self.data_path = data_path.encode("utf-8")
        self._load_library(lib_path)
        self.tts = None
        self.current_lang = None

    def _load_library(self, lib_path: str):
        """
        Loads the shared library and sets up the function prototypes for TTS operations.

        Args:
            lib_path (str): Path to the shared library.
        """
        self.lib = ctypes.cdll.LoadLibrary(lib_path)

        # Setup argument types and return types for library functions
        self.lib.create_tts.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.create_tts.restype = ctypes.c_void_p

        self.lib.synthesize_text.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.POINTER(ctypes.c_short)),
            ctypes.POINTER(ctypes.c_int),
        ]
        self.lib.synthesize_text.restype = ctypes.c_int

        self.lib.free_samples.argtypes = [ctypes.POINTER(ctypes.c_short)]
        self.lib.destroy_tts.argtypes = [ctypes.c_void_p]

        # Phonetic transcription: char* transcribe_text(tts, text, data_path, lang)
        self.lib.transcribe_text.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
        ]
        self.lib.transcribe_text.restype = ctypes.c_void_p
        self.lib.free_string.argtypes = [ctypes.c_void_p]

    def _recreate_tts(self, lang: str):
        """
        Recreates the TTS instance for a given language.

        Args:
            lang (str): The language code (e.g., 'eu' for Basque).

        Raises:
            RuntimeError: If the TTS instance could not be created.
        """
        if self.tts is not None:
            self.lib.destroy_tts(self.tts)
        self.tts = self.lib.create_tts(self.data_path, lang.encode("utf-8"))
        if not self.tts:
            raise RuntimeError(f"Failed to create TTS instance for language: {lang}")
        self.current_lang = lang

    def get_tts(self, text: str, lang: str = "eu", wav_path: Optional[str] = None) -> bytes:
        """
        Generates speech from text and returns it as a byte array, optionally saving it to a WAV file.

        Args:
            text (str): The text to be converted to speech.
            lang (str): The language code for TTS synthesis (default is 'eu' for Basque).
            wav_path (Optional[str]): If provided, saves the generated audio as a WAV file at this path.

        Returns:
            bytes: The generated audio as a byte array, or an empty byte array if synthesis fails.
        """
        text_bytes = text.encode("utf-8")
        lang_bytes = lang.encode("utf-8")

        # Check if the language is different from the current language
        if self.tts is None or self.current_lang != lang:
            self._recreate_tts(lang)

        samples_ptr = ctypes.POINTER(ctypes.c_short)()
        length = ctypes.c_int()

        success = self.lib.synthesize_text(
            self.tts, text_bytes, self.data_path, lang_bytes,
            ctypes.byref(samples_ptr), ctypes.byref(length)
        )

        # Free the native buffer whenever it was allocated, regardless of how we
        # leave this method -- including the empty/failed path and if numpy/wave
        # raise. `samples_ptr` is non-null once the C side has written it.
        if not samples_ptr:
            return b""
        try:
            if not success or length.value <= 0:
                return b""

            # Copy out of the native buffer (do NOT keep a view past free).
            samples_np = np.ctypeslib.as_array(samples_ptr, shape=(length.value,))
            samples_bytes = samples_np.astype(np.int16).tobytes()

            if wav_path:
                with wave.open(wav_path, "wb") as wf:
                    wf.setnchannels(1)            # Mono
                    wf.setsampwidth(2)            # 2 bytes per sample (16-bit)
                    wf.setframerate(self.SAMPLE_RATE)
                    wf.writeframes(samples_bytes)

            return samples_bytes
        finally:
            self.lib.free_samples(samples_ptr)

    def get_phonemes(self, text: str, lang: str = "eu", ipa: bool = False):
        """
        Phonetically transcribe text to SAMPA (or IPA) without synthesizing audio.

        Runs the full AhoTTS linguistic pipeline (number/date/abbreviation
        normalization, grapheme-to-phoneme, syllabification, lexical stress) in
        the bundled engine library and returns the phoneme transcription. It runs
        in-process via the shared library (no subprocess), so it does not need the
        standalone AhoTTS `modulo1y2` linguistic binary. For a dependency-free,
        pure-Python G2P matching a specific AhoTTS release, see the companion port
        project (ahotts-g2p).

        Args:
            text (str): Input text.
            lang (str): Language code ('eu' for Basque, 'es' for Spanish).
            ipa (bool): If True, map SAMPA phones to IPA via SAMPA_TO_IPA.

        Returns:
            list[list[str]]: One list of phones per word, in order. Lexical
            stress is carried as a leading "'" on the stressed phone. Returns
            an empty list if transcription fails.
        """
        text_bytes = text.encode("ISO-8859-15", "replace")
        lang_bytes = lang.encode("utf-8")

        if self.tts is None or self.current_lang != lang:
            self._recreate_tts(lang)

        ptr = self.lib.transcribe_text(self.tts, text_bytes, self.data_path, lang_bytes)
        if not ptr:
            return []
        raw = ctypes.cast(ptr, ctypes.c_char_p).value.decode("ISO-8859-15")
        self.lib.free_string(ptr)

        words = []
        for line in raw.split("\n"):
            line = line.strip()
            if not line:
                continue
            phones = line.split(" ")
            if ipa:
                phones = [self._sampa_to_ipa(p) for p in phones]
            words.append(phones)
        return words

    @staticmethod
    def _sampa_to_ipa(phone: str) -> str:
        """Map a single (optionally stress-marked) SAMPA phone to IPA."""
        stress = ""
        if phone.startswith("'"):
            stress, phone = "'", phone[1:]
        return stress + SAMPA_TO_IPA.get(phone, phone)

    def __del__(self):
        """
        Cleans up by destroying the TTS instance when the object is deleted.
        """
        if hasattr(self, 'tts') and self.tts:
            self.lib.destroy_tts(self.tts)
            self.tts = None


if __name__ == "__main__":
    tts = AhoTTS()

    audio_bytes = tts.get_tts("Kaixo Mundua!", lang="eu", wav_path="../output_eu.wav")

    if audio_bytes:
        print(f"Generated {len(audio_bytes)} bytes of audio.")

    audio_bytes = tts.get_tts("Hola Mundo", lang="es", wav_path="../output_es.wav")

    if audio_bytes:
        print(f"Generated {len(audio_bytes)} bytes of audio.")
