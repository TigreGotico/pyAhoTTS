"""Tests for AhoTTS.get_phonemes (phonetic transcription without synthesis)."""
import pytest
from pyahotts import AhoTTS, SAMPA_TO_IPA


@pytest.fixture(scope="module")
def tts():
    return AhoTTS()


def test_basic_sampa(tts):
    # "Bai" -> b 'a j  (stress on the nucleus a)
    out = tts.get_phonemes("Bai.", lang="eu")
    assert out == [["b", "'a", "j"]]


def test_multiword_structure(tts):
    out = tts.get_phonemes("Bai eta ez.", lang="eu")
    assert len(out) == 3                      # one list of phones per word
    assert all(isinstance(w, list) for w in out)
    assert out[0] == ["b", "'a", "j"]


def test_ipa_mapping(tts):
    sampa = tts.get_phonemes("Kaixo mundua!", lang="eu")
    ipa = tts.get_phonemes("Kaixo mundua!", lang="eu", ipa=True)
    assert len(sampa) == len(ipa) == 2
    # SAMPA "S" (kaixo's x) -> IPA "ʃ"
    assert "S" in sampa[0] and "ʃ" in ipa[0]
    # stress mark is preserved through the IPA conversion
    assert any(p.startswith("'") for w in ipa for p in w)


def test_empty_input(tts):
    assert tts.get_phonemes("", lang="eu") == []


def test_transcribe_then_synthesize_no_crash(tts):
    # regression: transcribing without ever synthesizing must not corrupt the
    # engine state (the HTS engine is only initialized in the synthesis path).
    tts.get_phonemes("Kaixo.", lang="eu")
    audio = tts.get_tts("Kaixo.", lang="eu")
    assert isinstance(audio, bytes) and len(audio) > 0


def test_sampa_to_ipa_table():
    assert SAMPA_TO_IPA["s`"] == "ʂ"
    assert SAMPA_TO_IPA["tS"] == "tʃ"
