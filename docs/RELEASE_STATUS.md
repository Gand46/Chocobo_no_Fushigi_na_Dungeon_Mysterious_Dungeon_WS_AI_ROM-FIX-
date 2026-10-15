# HF20 TEST status (QA27)

- Original Japanese input: 2,097,152 bytes, CRC32 CCAA4853, SHA-256 `38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728`.
- HF20 target SHA-256: `030de69bc2c6e8870fa2650fe879d7f6003c4c5580c5b22def48f08f875b8c49`.
- HF20 BPS SHA-256: `173c985a3c92158609ac02b1e201916840a0c314fe5ba9d128fef132dff78181`.
- QA26 visual: 14 resources, 12 excess spaces, six reflows, 28 native sessions, 18 paired pages, zero nonblank dropped characters. Review by coordinator and Astra, scoped to those resources.
- QA27 runtime: 8 new HF19/HF20 paired sessions, 89 checks; byte-identical 32 KiB protected saves; two exact 2,516-byte cold-load copies; six inventory cases and assisted boss matched; 56 captures per version identical.
- HF19→HF20: 352 changed bytes limited to 14 story spans and checksum; getters, pointers, native font and executable code unchanged. HF20 remains TEST.
- Current source recipe: `build.py`, `src/legacy_translation_ranges.json`, `src/corrections.json`, `qa26/adjustments.json`, `qa26/rebuild_edits.py`, historical checked HF19 source at `docs/history/qa25/`.
- Incomplete globally: some visual spacing remains, natural host/event routes, entire getters/graphics audit, full natural playthrough, second emulator and physical hardware. `FINAL_APPROVED=false` in `docs/approval_matrix.json`.
