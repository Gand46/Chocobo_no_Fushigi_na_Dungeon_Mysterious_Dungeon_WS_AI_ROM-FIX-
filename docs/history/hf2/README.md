# Chocobo WonderSwan — English v1.1 + HF2 TEST

Experimental cumulative translation and bug mitigation. Apply `patches/Chocobo_EN_v1.1_HF2_TEST_JP_CCAA4853.bps` directly to the 2 MiB Japanese ROM (CRC32 CCAA4853). Output CRC32 A18CFFA6, WS checksum F2E4. No ROM or emulator is included.

HF2 includes all ten HF1 text corrections and a guard against the reproducible Lafoss freeze: the sprite renderer must not index a descriptor using model FFFF. It skips the absent graphic via the native cleanup path. **The missing spell animation and full spell semantics are not reconstructed.** This is TEST, not RC and not a global save-safety claim. Whistle rendering and late-game event reports remain open.

## Build

Python 3.10+; no nonstandard package required for build and unit tests.

```text
python3 build.py /path/to/Japanese.ws --out build
python3 -m unittest discover -s tests -v
python3 tools/verify_evidence.py /path/to/Japanese.ws
```

Windows: `BUILD.bat "C:\path\Japanese.ws"`. macOS: `BUILD.command` with the ROM path. Launchers are included; only Linux execution was tested here. The --development option is for intentional source edits; the pinned build verifies the release hash by default. Never use a translated ROM as input.

## Sources and evidence

- `src/legacy_translation_ranges.json`: exact reconstruction of v1.1, recovered from user-supplied binaries; not the original translators' source.
- `src/corrections.json`: all HF1 and HF2 edits, exact preimages and reasons.
- `src/invalid_model_guard.asm`, `tools/generate_guard.py`: editable implementation of the new guard.
- `localization/`, `formats/`: corrected text and observed format details.
- `qa/`, `qa3/`: resource, menu, item, capture and cold-load tests. `qa2_legacy/` is retained only as prior evidence.
- `evidence/`: traces, screenshots, savestates, native saves, provenance, old HF1 validation and new HF2 results. Historical evidence is not silently promoted to HF2 coverage.
- `INFORME_ES.md`: findings, limits, reproduction commands and next actions.

The cumulative BPS was checked against the build and an independent BPS decoder. Native saving and cold loading passed a basic HF2 Mesen case. See the report for the scope of synthetic evidence, control cases and unresolved reports. Original game code is not invented or claimed to have been recovered in full.

Preserve original translation credits in `docs/LEGACY_README.txt`. Original game/assets belong to their respective owners; the new project additions are identified separately. Back up existing saves before testing this experimental build.
