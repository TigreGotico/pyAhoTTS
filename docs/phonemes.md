# Phonemes (phonetic transcription)

`get_phonemes()` exposes the AhoTTS linguistic front end as phonemes without
synthesizing audio, so it can be used as a grapheme-to-phoneme (G2P) component on
its own.

```python
from pyahotts import AhoTTS, SAMPA_TO_IPA
tts = AhoTTS()
tts.get_phonemes("Kaixo mundua!", lang="eu", ipa=True)
# [['k', 'a', 'j', 'ʃ', "'o"], ['m', 'u', 'n', 'd', "'u", 'a']]
```

## Output format

- A **list of words**; each word is a **list of phone tokens** in order.
- **Lexical stress** is a leading `'` on the stressed nucleus (e.g. `"'o"`).
- Phones are **SAMPA** by default, or **IPA** when `ipa=True`.

## How it is produced

Internally the engine runs the full linguistic pipeline and the transcription is
read off the resolved utterance:

```
text
 → normalization (numbers, dates, abbreviations)
 → grapheme-to-phoneme (digraphs tt, dd, tx, ts, tz, ll, rr, x, z, s, …)
 → syllabification
 → lexical stress assignment
 → SAMPA phone names (canonical, from the engine's phone table)
```

The native side walks the utterance one word at a time, emitting the canonical
SAMPA for each phone (via the engine's `phone_tosampa` table — **not** the
HTS-label remaps used for the acoustic model, so e.g. `z`→`s\`` and `tz`→`ts\``
are preserved), with `'` prefixed on stressed nuclei. Pause/silence phones are
dropped; word boundaries separate the lists.

## SAMPA → IPA

`ipa=True` maps each phone through `SAMPA_TO_IPA` (importable from `pyahotts`).
The mapping matches the one shipped with the Aholab phonemizer:

| SAMPA | IPA | | SAMPA | IPA | | SAMPA | IPA |
|---|---|---|---|---|---|---|---|
| `g` | ɡ | | `tS` | tʃ | | `ts\`` | tʂ |
| `B` | β | | `D` | ð | | `G` | ɣ |
| `T` | θ | | `s\`` | ʂ | | `S` | ʃ |
| `J` | ɲ | | `L` | ʎ | | `r` | ɾ |
| `rr` | r | | `jj` | ʝ | | `gj` | ɟ |

(Full table in `pyahotts.SAMPA_TO_IPA`.) Stress marks are preserved across the
conversion.

## Notes & limitations

- The transcription reflects the **bundled engine version** (V1 — see
  [Versions](versions.md)). Other AhoTTS releases phonemize slightly differently
  (diphthong glides, stress, dictionary exceptions); pin behavior with the
  [golden tests](testing.md).
- AhoTTS is the *engine*; if you need a pure-Python, dependency-free G2P that
  matches a specific AhoTTS version, see the companion port project.
</content>
