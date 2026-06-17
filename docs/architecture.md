# Architecture

pyAhoTTS is a thin `ctypes` binding over the native **`libhtts`** library compiled
from the AhoTTS C/C++ sources in `src/`.

```
your code
   │  AhoTTS.get_tts / get_phonemes        (pyahotts/__init__.py)
   ▼
ctypes  ──►  libhtts.so                      (src/, built via CMake)
                 │
                 ├─ linguistic front end (eu_*/es_* : normalization, G2P,
                 │     syllabification, stress)  →  utterance of phones
                 ├─ HTS acoustic engine          →  parameter streams
                 └─ AhoCoder vocoder             →  waveform
```

## Python surface (`pyahotts/__init__.py`)

`AhoTTS` loads `libhtts` with `ctypes.cdll`, declares the C prototypes, and
exposes `get_tts`, `get_phonemes`, plus the `SAMPA_TO_IPA` table. It converts the
returned `c_short` sample buffer into NumPy `int16`, writes WAV when asked, and
recreates the engine instance when the language changes.

## Exported C API (`src/htts_wrapper.cpp`)

| symbol | purpose |
|---|---|
| `create_tts(data_path, lang)` | build an engine for a language (loads its dictionary) |
| `synthesize_text(tts, text, data_path, lang, &samples, &len)` | text → `int16` samples |
| `transcribe_text(tts, text, data_path, lang) -> char*` | text → SAMPA, one word per line, stress as `'` |
| `free_samples(short*)` / `free_string(char*)` | free engine-allocated buffers |
| `destroy_tts(tts)` | free the engine |

## The transcription path

`transcribe_text` reuses the engine's linguistic stage and stops before acoustic
synthesis. It runs `input_multilingual` then walks the resolved utterance with
`HTS_U2W::pho2sampa`, emitting canonical SAMPA per phone (`phone_tosampa`), one
word per line, stress as a leading `'`. Because no voice models are loaded on this
path, the destructor guards `HTS_Engine_clear` with an "engine initialized" flag —
otherwise transcribing (or merely creating an engine) and then destroying it would
free uninitialized pointers.

## Data layout (`data_tts/`)

```
data_tts/
  dicts/   eu_dicc.dic, es_dicc.dic        # linguistic dictionaries
  voices/  aholab_eu_female/, aholab_es_female/   # HTS voice models
```

`data_path` defaults to the packaged `data_tts`; override it to point at custom
dictionaries/voices.
</content>
