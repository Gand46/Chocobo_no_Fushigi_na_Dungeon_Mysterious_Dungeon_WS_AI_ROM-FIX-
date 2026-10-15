# Chocobo English v1.1 + HF3 TEST

Cumulative reconstructed editable patch sources. Apply the current BPS directly to the clean Japanese ROM (CRC32 CCAA4853), never on top of an earlier translation/patch.

HF3 preserves the ten HF1 text fixes and HF2 invalid-model guard, and repairs the Whistle resource: complete solid tiles and normalize palette aliases. The original 37 graphic tiles and native font are unchanged. See INFORME_ES.md for evidence, reproduction commands and limitations.

Physical cartridge failure: the user established a separate electrical cause; it is outside this ROM audit.

TEST, not RC. Lafoss full animation/damage, title translation, global layout, advanced events, second emulator and hardware remain unvalidated. Current authority: manifest.json, src/corrections.json and docs/issue_register.csv. Historical reports are retained only as history.

Build: `python3 build.py /path/JP.ws --out /path/new_output`.
No commercial ROM is included. Full cumulative editable translation recipe, fixes, builder, BPS and QA evidence are included.
