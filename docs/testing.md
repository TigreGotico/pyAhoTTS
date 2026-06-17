# Testing

The suite lives in `test/` and runs with `pytest`:

```bash
pip install -e .[test]
pytest test/ -q
```

## What is tested

- **Unit** (`test/test_phonemes.py`) — `get_phonemes` output shape, SAMPA/IPA
  mapping, stress marks, empty input, and that transcribing then synthesizing does
  not corrupt engine state.
- **End-to-end** (`test/test_e2e.py`) — golden tests that pin the engine's
  behavior:
  - `test_phonemes_match_v1_golden` — `get_phonemes` must reproduce the committed
    **V1** transcriptions verbatim.
  - `test_synthesis_produces_audio` — `get_tts` yields a non-trivial waveform.
  - `test_spanish_synthesis_smoke` — Spanish path produces audio.

## Golden fixtures

`test/fixtures/v1_golden_eu.json` holds the expected V1 text→phoneme pairs (and
audio size floors). Because pyAhoTTS is a binding, these goldens are the contract
that the bundled native library keeps matching the upstream **V1** AhoTTS release
(see [Versions](versions.md)) across rebuilds and architectures.

### Regenerating

Only regenerate when the engine legitimately changes, and **review the diff**:

```python
import json
from pyahotts import AhoTTS
t = AhoTTS()
corpus = [...]   # the sentences in the fixture
golden = {"phonemes": {s: t.get_phonemes(s, lang="eu", ipa=True) for s in corpus},
          "audio_min_bytes": {...}}
json.dump(golden, open("test/fixtures/v1_golden_eu.json", "w"),
          ensure_ascii=False, indent=1)
```

## CI

Pull requests run the shared `OpenVoiceOS/gh-automations` reusable workflows:
build-tests (matrix Python versions), coverage, lint, license-check, pip-audit,
repo-health, and release-preview. The golden e2e tests run as part of build-tests,
so any drift of the bundled binding versus upstream V1 fails CI without needing to
rebuild the upstream sources.
</content>
