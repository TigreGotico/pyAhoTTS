# Licensing & credits

pyAhoTTS carries a **split license**. The Python wrapper, the upstream engine
code, and the bundled voice and linguistic data are licensed differently.

| Component | License |
|---|---|
| Python wrapper (`pyahotts/__init__.py`, packaging) | MIT |
| AhoTTS engine sources (`src/`, compiled to `libhtts`) | GPL-3.0+ (Aholab / UPV-EHU) |
| Voice models & linguistic data (`data_tts/`, dictionaries) | CC BY-SA 3.0 (Aholab / UPV-EHU) |

See `COPYRIGHT_and_LICENSE_code.txt` and `COPYRIGHT_and_LICENSE_voices.txt` in the
repository root for the authoritative terms. Because the distributed library links
the GPL-3.0+ engine, the GPL-3.0+ governs redistribution of the **binary**
package. The MIT wrapper code may be reused under MIT.

## Credits

- **AhoTTS**: Aholab Signal Processing Laboratory, University of the Basque
  Country (UPV/EHU). Linguistic processing for Basque and Spanish, and the
  AhoCoder vocoder. For upstream sources and releases, see [Versions](versions.md).
- Python bindings build on the [ekaitz-zarraga/AhoTTS](https://github.com/ekaitz-zarraga/AhoTTS)
  fork. The Ministerio para la Transformación Digital y de la Función Pública
  and the Plan de Recuperación, Transformación y Resiliencia funded the
  bindings. The EU (NextGenerationEU) funded this work within the ILENIA
  project (ref. 2022/TL22/00215337).

---
[← Testing](testing.md) · [Home](README.md)
