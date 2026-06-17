# Installation

## From PyPI

```bash
pip install pyahotts
```

The wheel bundles the native library (`libhtts`) for `x86_64` and `aarch64` Linux,
plus all voice and dictionary data, so nothing needs to be compiled. The only
runtime dependency is `numpy`.

```python
from pyahotts import AhoTTS
tts = AhoTTS()                       # loads the bundled libhtts for your arch
tts.get_tts("Kaixo!", lang="eu", wav_path="out.wav")
```

## From source

```bash
git clone https://github.com/TigreGotico/pyAhoTTS
cd pyAhoTTS
pip install .            # or: pip install -e .[test]   to run the test suite
```

## Building the native library

The prebuilt `.so` files live in `pyahotts/` (`libhtts_x86_64.so`,
`libhtts_aarch64.so`). To rebuild from the C/C++ sources in `src/`:

```bash
mkdir build && cd build
cmake ..                 # add -DCMAKE_POLICY_VERSION_MINIMUM=3.5 on CMake >= 4
make -j"$(nproc)"
cp src/libhtts.so ../pyahotts/libhtts_<arch>.so
```

For an architecture without a bundled `.so` (e.g. 32-bit x86), build it and pass
the path explicitly:

```python
tts = AhoTTS(lib_path="/path/to/libhtts.so")
```

See [Building libhtts](building.md) for details on the build and the exported C API.

## Supported platforms

Linux `x86_64` and `aarch64` are shipped prebuilt. macOS/Windows are not bundled;
build `libhtts` for your platform and pass `lib_path`.
</content>
