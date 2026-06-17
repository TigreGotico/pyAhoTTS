# Licensing & credits

pyAhoTTS carries a **split license** — the Python wrapper, the upstream engine
code, and the bundled voice/linguistic data are licensed differently.

| Component | License |
|---|---|
| Python wrapper (`pyahotts/__init__.py`, packaging) | MIT |
| AhoTTS engine sources (`src/`, compiled to `libhtts`) | GPL-3.0+ (Aholab / UPV-EHU) |
| Voice models & linguistic data (`data_tts/`, dictionaries) | CC BY-SA 3.0 (Aholab / UPV-EHU) |

See `COPYRIGHT_and_LICENSE_code.txt` and `COPYRIGHT_and_LICENSE_voices.txt` in the
repository root for the authoritative terms. Because the distributed library links
the GPL-3.0+ engine, redistribution of the **binary** package is governed by the
GPL-3.0+; the MIT wrapper code may be reused under MIT.

## Credits

- **AhoTTS** — Aholab Signal Processing Laboratory, University of the Basque
  Country (UPV/EHU). Linguistic processing for Basque and Spanish, and the
  AhoCoder vocoder. Upstream sources and releases: see [Versions](versions.md).
- Python bindings build on the [ekaitz-zarraga/AhoTTS](https://github.com/ekaitz-zarraga/AhoTTS)
  fork and were funded by the *Ministerio para la Transformación Digital y de la
  Función Pública* and the *Plan de Recuperación, Transformación y Resiliencia* —
  funded by the EU (NextGenerationEU) within the ILENIA project (ref.
  2022/TL22/00215337).
</content>
