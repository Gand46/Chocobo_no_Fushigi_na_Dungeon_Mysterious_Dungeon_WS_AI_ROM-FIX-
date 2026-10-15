# Repository layout and contribution

The intended public home is [Gand46/Chocobo_no_Fushigi_na_Dungeon_Mysterious_Dungeon_WS_AI_ROM-FIX-](https://github.com/Gand46/Chocobo_no_Fushigi_na_Dungeon_Mysterious_Dungeon_WS_AI_ROM-FIX-). The current tracked source tree is the curated HF20 TEST export. Keep code and editable data in their established `src/`, `qa*/`, `tools/`, `formats/`, `localization/` and `assets/` paths so existing imports and the build recipe remain valid.

- `README.md`, `build.py`, `BUILD.bat`, `BUILD.command`: entry points for contributors.
- `patches/`: cumulative HF20 BPS and historical patches; apply only the HF20 BPS directly to the identified Japanese original.
- `docs/`: provenance, credits, original ROM repairs, history, status, evidence index and historical phase documentation. Earlier visual reports are in `docs/reports/`; QA26 and QA27 reports are linked from the README.
- `evidence/qa26_runs/`: the current native traces required by `qa26/verify_scope.py`.
- `support/`: controlled historical native evidence and the separate QA27 regression bundle. Run `python3 tools/restore_historical_evidence.py --to restored` to unpack the former into an ignored inspection directory.
- `GITHUB_PACKAGE_MANIFEST.json`: checked inventory of the tracked source export; it is distinct from the full 115,444-file formal continuity snapshot.

Verify `python3 tools/verify_github_export.py .` before making edits. With a private clean JP ROM, run `python3 build.py /path/Japanese.ws --out build`, `CONTINUITY_INPUT_JP=/path/Japanese.ws python3 qa26/release_build.py`, `CONTINUITY_INPUT_JP=/path/Japanese.ws python3 qa26/verify_scope.py`, and `python3 -m unittest discover -s tests -v`. Save new semantic changes in editable recipes, rebuild, and update the manifest only after documenting the changed files and checking the new output. Never commit the JP ROM, generated English ROM, BIOS or a personal save. Controlled synthetic `.sav` fixtures already present in the project have stated QA provenance.

The original v1.1 translation team is credited in `docs/UPSTREAM_TRANSLATION.md` and the root README. The reconstructed English baseline is not their original source code. No blanket license to the original game or the user's title art is implied.

At this checkpoint the curated commit is local: this environment's Git push failed for lack of credentials. The full source ZIP and Git bundle are preserved separately. Once an authenticated Git transport is available, check the current `origin/main` head, then push the curated `main` commit. Do not overwrite an intervening remote commit; integrate it first if the head changed.
