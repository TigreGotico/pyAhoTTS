# Usage

Everything is exposed through a single class, `AhoTTS`.

```python
from pyahotts import AhoTTS

tts = AhoTTS()
```

## `AhoTTS(lib_path=None, data_path=...)`

| arg | default | meaning |
|---|---|---|
| `lib_path` | bundled `libhtts_<machine>.so` | path to the native library; override for unbundled architectures |
| `data_path` | `<package>/data_tts` | directory holding `dicts/` and `voices/` |

The underlying engine instance is created lazily and **recreated automatically
when the language changes** between calls.

## Synthesis — `get_tts(text, lang="eu", wav_path=None) -> bytes`

Generates speech and returns raw **16-bit mono PCM @ 16 kHz** bytes. If `wav_path`
is given, a WAV file is also written.

```python
audio = tts.get_tts("Kaixo mundua!", lang="eu", wav_path="eu.wav")
audio = tts.get_tts("Hola mundo",   lang="es", wav_path="es.wav")
print(len(audio), "bytes")          # empty bytes on failure
```

- `lang`: `"eu"` (Basque) or `"es"` (Spanish).
- Returns `b""` if synthesis fails (never raises for empty output).

### Numpy / custom playback

The bytes are little-endian `int16`:

```python
import numpy as np
samples = np.frombuffer(tts.get_tts("Kaixo!"), dtype=np.int16)
```

## Phonemization — `get_phonemes(text, lang="eu", ipa=False) -> list[list[str]]`

Runs **only the linguistic front end** (normalization → grapheme-to-phoneme →
syllabification → lexical stress) and returns the phonetic transcription, with no
audio synthesis — the AhoTTS linguistic analysis exposed directly, without the
acoustic stage.

```python
tts.get_phonemes("Bai eta ez.", lang="eu")
# [['b', "'a", 'j'], ['e', 't', 'a'], ["'e", 's`']]

tts.get_phonemes("Bai eta ez.", lang="eu", ipa=True)
# [['b', "'a", 'j'], ['e', 't', 'a'], ["'e", 'ʂ']]
```

- Returns **one list of phones per word**, in order.
- **Lexical stress** is carried as a leading `'` on the stressed phone.
- `ipa=False` → SAMPA phones; `ipa=True` → IPA via the [`SAMPA_TO_IPA`](phonemes.md) table.
- Returns `[]` if transcription fails.

Number/date/abbreviation **normalization happens inside the engine**, so digits
and abbreviations are expanded before phonemization (e.g. dates, ordinals).

See [Phonemes](phonemes.md) for the phone inventory, the SAMPA→IPA mapping, and
how the transcription relates to the AhoTTS linguistic stages.

## Languages & voices

| lang | dictionary | bundled voice |
|---|---|---|
| `eu` | `data_tts/dicts/eu_dicc` | `aholab_eu_female` |
| `es` | `data_tts/dicts/es_dicc` | `aholab_es_female` |

## Text encoding

Input text is encoded to **ISO-8859-15** before reaching the engine (AhoTTS is a
legacy ISO-8859-15 codebase). Characters outside that set are replaced; standard
Basque/Spanish text is fully covered.
</content>
