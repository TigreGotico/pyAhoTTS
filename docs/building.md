# Building libhtts

The native library is built from the C/C++ sources in `src/` with CMake. Prebuilt
`.so` files are committed under `pyahotts/` (`libhtts_x86_64.so`,
`libhtts_aarch64.so`) and shipped in the wheel; you only need to build when
porting to a new architecture or changing the engine.

## Build

```bash
mkdir build && cd build
cmake ..                                   # CMake >= 4: add -DCMAKE_POLICY_VERSION_MINIMUM=3.5
make -j"$(nproc)"
# result: build/src/libhtts.so
```

Install it into the package for your architecture:

```bash
cp src/libhtts.so ../pyahotts/libhtts_$(uname -m).so
```

The top-level `CMakeLists.txt` builds `libhtts` from `src/CMakeLists.txt` and
installs the `data_tts` tree.

## Per-architecture notes

- `uname -m` selects the bundled library at runtime (`libhtts_<machine>.so`).
- Only `x86_64` and `aarch64` are committed. For other targets, build and pass
  `AhoTTS(lib_path=...)`.
- **When you change the C sources, rebuild *every* shipped architecture** (a CI
  matrix or cross-build), not just the host one — otherwise the other arch's
  bundled `.so` goes stale.

## Exported symbols

The build exposes the C API consumed by the Python binding — see
[Architecture](architecture.md): `create_tts`, `synthesize_text`,
`transcribe_text`, `free_samples`, `free_string`, `destroy_tts`.

## Regenerating phoneme golden fixtures

If an engine change legitimately alters transcriptions, regenerate the e2e golden
fixtures from a **verified** build and review the diff — see [Testing](testing.md).
</content>
