# Chocobo HF20 TEST — GitHub export context

Authority: formal HF20 QA26 source snapshot `1eb14098df9f00f9e583b74ed32ba75914af21087e1ea520bec0f1ef51042571`; active patch SHA-256 `173c985a3c92158609ac02b1e201916840a0c314fe5ba9d128fef132dff78181`; target ROM SHA-256 `030de69bc2c6e8870fa2650fe879d7f6003c4c5580c5b22def48f08f875b8c49`.

The package carries all editable cumulative sources, release reports and selected native evidence. The full-source authority and export omissions are described in `docs/SOURCE_PROVENANCE.md`. To resume, verify `GITHUB_PACKAGE_MANIFEST.json`, then rebuild from the clean JP input with `qa26/release_build.py` and run 13 project unit tests. Do not treat this subset of historical raw evidence as the original full snapshot or use an older HF release as a base.

QA27 added only validation, no ROM bytes: native protected save/cold load, six inventory cases and assisted combat matched HF19 exactly in eight new sessions (89 checks, 56 capture pairs). QA26's cosmetic review remains scoped; `FINAL_APPROVED=false`. Original Japanese bug fixes and unresolved reports are separated in `docs/ORIGINAL_ROM_FIXES.md`; current unresolved contexts in `docs/RELEASE_STATUS.md`.

Upstream English v1.1 attribution: `docs/UPSTREAM_TRANSLATION.md` links the Romhacking.net listing and transcribes the preserved `docs/LEGACY_README.txt` credits. The packaged `src/legacy_translation_ranges.json` is a reconstruction, while `src/legacy_v1.1_original.ips` is the preserved legacy patch. HTML reports QA26/QA27 link back to this provenance.

GitHub destination: `Gand46/Chocobo_no_Fushigi_na_Dungeon_Mysterious_Dungeon_WS_AI_ROM-FIX-`, a public repository created after the original ZIP export. This checkout keeps the 28 QA26 native runs browsable and archives 5,766 earlier evidence files without dropping them. The original ZIP remains separately saved; see `docs/REPOSITORY_CLEANUP.md` for the precise migration and verification scope.

Publication checkpoint: the curated tree has a local commit and passes its exact inventory, ROM rebuild, scoped QA26 checks and 13 unit tests. `git push origin main` was attempted but the local Git transport requested GitHub credentials that are unavailable in this environment. The remote still points to its initial commit `60064d1efeade46ed281d58c1d9e714c7c6f6d32`. Do not claim the curated tree is already published; use the saved source ZIP and Git bundle or an authenticated Git push to promote this exact checked commit.
