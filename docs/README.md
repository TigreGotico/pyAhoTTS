# pyAhoTTS documentation

Python bindings for [AhoTTS](https://github.com/aholab/AhoTTS), the Text-to-Speech
system for **Basque (`eu`)** and **Spanish (`es`)** developed by the Aholab Signal
Processing Laboratory at the University of the Basque Country (UPV/EHU). AhoTTS
pairs a linguistic front end (normalization → grapheme-to-phoneme →
syllabification → lexical stress) with an HTS-based acoustic engine and the
AhoCoder vocoder.

`pyahotts` wraps the compiled engine (`libhtts`) via `ctypes` and ships the native
library plus all voice/dictionary data inside the wheel, so you can synthesize
speech — and now obtain phonetic transcriptions — without compiling anything.

```python
from pyahotts import AhoTTS

tts = AhoTTS()
tts.get_tts("Kaixo mundua!", lang="eu", wav_path="out.wav")   # text -> audio
tts.get_phonemes("Kaixo mundua!", lang="eu", ipa=True)        # text -> phonemes
# [['k', 'a', 'j', 'ʃ', "'o"], ['m', 'u', 'n', 'd', "'u", 'a']]
```

## Contents

- [Installation](installation.md) — pip install, and building `libhtts` from source.
- [Usage](usage.md) — the `AhoTTS` API: synthesis and phonemization.
- [Phonemes](phonemes.md) — phonetic transcription, SAMPA/IPA, stress, the SAMPA→IPA table.
- [Architecture](architecture.md) — how the binding and the C engine fit together.
- [Building libhtts](building.md) — the CMake build, the C API, per-architecture `.so` notes.
- [Versions & source of truth](versions.md) — the AhoTTS V1/V2/V3 lineage and what pyAhoTTS bundles.
- [Testing](testing.md) — unit + end-to-end golden tests, regenerating fixtures, CI.
- [Licensing](licensing.md) — the split license and credits.

## At a glance

| | |
|---|---|
| Languages | Basque (`eu`), Spanish (`es`) |
| Synthesis output | 16-bit mono PCM WAV @ 16 kHz |
| Phoneme output | per-word phone lists, SAMPA or IPA, lexical stress as a leading `'` |
| Native lib | `libhtts` (bundled `.so` for `x86_64` and `aarch64`) |
| Runtime deps | `numpy` only |
| Internal text encoding | ISO-8859-15 |
</content>
