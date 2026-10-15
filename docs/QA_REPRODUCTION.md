# QA reproduction — HF2

See ../INFORME_ES.md for exact fixture meanings, limits, cold-load steps and rejected attempts. All runs identify the input ROM SHA-256, state SHA-256 (null for cold boot), plan and driver hashes. `evidence/qa3_provenance.json` links checkpoints.

Use Mesen 2.1.1 Linux x86_64 (hash in manifest.json), its own portable folder with settings.json, and separate disposable Saves directories for simultaneous runs. Configure no external BIOS requirement for WS. The Mesen binaries are not included.

```text
python3 qa3/run.py path/to/HF2.ws evidence/qa3/q3_dungeon/checkpoint.mss qa3/lafoss_use.lua new_output --mesen /path/to/Mesen --timeout 25
python3 qa/run_suite.py path/to/HF2.ws evidence/checkpoints/HF1_TEST_town.mss new_resource_output --mesen /path/to/Mesen --suite resources --timeout 90
```

Native saves in `evidence/qa3/q3_hf2_save/native_save/` were created by confirming Yes in the game. For cold-load reproduction use a new process, name the ROM `Chocobo_EN_v1.1_HF2_TEST.ws`, copy its `.sav`/`.ieeprom` to that portable emulator's Saves folder, pass `-` as the state and `qa3/cold_verified.lua` as the plan. No emulation state is loaded during this test. Do not confuse the state subsequently saved at the end with the source of the loading process.

QA2's final capture callback was not one-shot; its failed cold-loading attempts are invalid evidence against the ROM. Use QA3. `loaded.png` from the pre-first-frame snapshot is intentionally excluded because Mesen had no completed framebuffer at that point. The other frame PNGs are actual rendered evidence.

`ADD_DRINK=1` is required for q3_dispel_after_verified / q3_hf2_dispel_after and is documented in the report; earlier run.json files did not record this variable. No other fixture parameter was used in the published runs.
