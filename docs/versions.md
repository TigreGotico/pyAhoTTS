# Versions & source of truth

AhoTTS is developed upstream by **Aholab (UPV/EHU)**. It has evolved through
several releases, and — importantly — **different releases phonemize the same text
differently** (diphthong glides, lexical stress, dictionary exceptions). When
phonemes must match a model that was trained with a particular release, the
release matters.

**The upstream AhoTTS source repositories are the source of truth.** `pyahotts` is
*our* binding: it wraps a build of one specific upstream release and is validated
against it (see [Testing](testing.md)). It is not itself the reference.

## The lineage

| | Release | Upstream source | Notes |
|---|---|---|---|
| **V1** | Original AhoTTS | [ekaitz-zarraga/AhoTTS](https://github.com/ekaitz-zarraga/AhoTTS) (= [aholab/AhoTTS](https://github.com/aholab/AhoTTS) before its Dec-2025 rewrite) | Classic linguistic front end; rule-based stress. **This is what pyAhoTTS bundles.** |
| **V2** | VITS-era rewrite | [aholab/AhoTTS](https://github.com/aholab/AhoTTS) (current HEAD) | Restructured engine; revised diphthong/stress rules. Powers the [HiTZ VITS voices](https://huggingface.co/collections/HiTZ/tts). |
| **V3** | StyleTTS-era | [hitz-zentroa/aHoTTS](https://github.com/hitz-zentroa/aHoTTS) | Newer dictionary + transcription tweaks. Used to phonemize [HiTZ/StyleTTS2-eu](https://huggingface.co/HiTZ/StyleTTS2-eu). |

(In practice V1 and V2 differ by exactly the Dec-2025 commit on `aholab/AhoTTS`;
"V1" is that repo with the last commit excluded.)

## What pyAhoTTS provides

pyAhoTTS bundles and exposes **V1**. Its `get_phonemes` / `get_tts` reproduce the
V1 engine's behavior, locked down by golden [end-to-end tests](testing.md) so the
bundled binding cannot silently drift from the upstream V1 source.

If you need V2 or V3 behavior, that must come from the corresponding upstream
release — pyAhoTTS does not currently embed those.

## Picking a version

- Synthesizing speech for general use → V1 (this package) is fine.
- Producing phonemes to feed a **specific pretrained model** → use the release that
  model was trained with (e.g. a StyleTTS2-eu model expects V3-style phonemes).
  Matching the wrong release yields slightly out-of-distribution input.
</content>
