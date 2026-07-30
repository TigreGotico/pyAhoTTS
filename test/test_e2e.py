"""End-to-end tests for pyAhoTTS.

pyAhoTTS is a binding that bundles a build of the upstream AhoTTS **V1** engine
(ekaitz-zarraga/AhoTTS = aholab/AhoTTS before the Dec-2025 rewrite). The upstream
binary is the source of truth; these golden fixtures capture its V1 behavior, and
these tests assert our bundled binding keeps reproducing it exactly across
rebuilds / platforms.

Fixtures: test/fixtures/v1_golden_eu.json  (regenerate from a verified upstream
V1 build if the engine is ever updated).
"""
import json
import os

import pytest
from pyahotts import AhoTTS

FIX = os.path.join(os.path.dirname(__file__), "fixtures", "v1_golden_eu.json")


@pytest.fixture(scope="module")
def golden():
    with open(FIX, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def tts():
    return AhoTTS()


def test_phonemes_match_v1_golden(tts, golden):
    """get_phonemes must reproduce the upstream V1 transcription verbatim."""
    mism = []
    for text, expected in golden["phonemes"].items():
        got = tts.get_phonemes(text, lang="eu", ipa=True)
        if got != expected:
            mism.append((text, got, expected))
    assert not mism, "phoneme drift vs V1 golden:\n" + "\n".join(
        f"  {t}\n    got={g}\n    exp={e}" for t, g, e in mism
    )


def test_synthesis_produces_audio(tts, golden):
    """get_tts must produce a non-trivial waveform for each sentence."""
    for text, min_bytes in golden["audio_min_bytes"].items():
        audio = tts.get_tts(text, lang="eu")
        assert isinstance(audio, bytes)
        assert len(audio) >= min_bytes, f"{text!r}: {len(audio)} < {min_bytes}"


def test_spanish_synthesis_smoke(tts):
    audio = tts.get_tts("Hola mundo.", lang="es")
    assert isinstance(audio, bytes) and len(audio) > 0
