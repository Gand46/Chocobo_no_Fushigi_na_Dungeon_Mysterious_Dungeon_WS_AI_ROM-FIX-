# Chocobo no Fushigi na Dungeon — WonderSwan English translation

**Current version: v1.1 HF20 TEST.** This repository contains editable cumulative patch sources, the direct Japanese-to-English BPS, the visual reports, change history, selected native runtime evidence, and a reproducible build. The current patch remains a test build; global visual approval, a complete natural playthrough, hardware testing and a second emulator are outstanding.

## Apply the patch

Apply [`patches/Chocobo_EN_v1.1_HF20_TEST_JP_CCAA4853.bps`](patches/Chocobo_EN_v1.1_HF20_TEST_JP_CCAA4853.bps) **directly** to a clean Japanese 2,097,152-byte WonderSwan ROM with CRC32 `CCAA4853` and SHA-256 `38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728`. Do not chain earlier HF patches or apply the patch to another English ROM.

| File | SHA-256 |
| --- | --- |
| HF20 BPS | `173c985a3c92158609ac02b1e201916840a0c314fe5ba9d128fef132dff78181` |
| Expected reconstructed HF20 ROM | `030de69bc2c6e8870fa2650fe879d7f6003c4c5580c5b22def48f08f875b8c49` |

No game ROM, BIOS or emulator is distributed here.

## Rebuild and edit

Python 3.10+ is needed; the build itself uses Python's standard library. On Windows, run `BUILD.bat "C:\path\Japanese.ws"`. On macOS, use `BUILD.command "/path/Japanese.ws"`. On Linux, run `python3 build.py /path/Japanese.ws --out build` and `python3 -m unittest discover -s tests -v`. The batch and command launchers invoke the same checked builder. It verifies the Japanese SHA-256, every source preimage, the final ROM hash and an independent BPS round trip. The output is `build/Chocobo_EN_v1.1_HF20_TEST.ws`; this private output is ignored by Git.

`src/legacy_translation_ranges.json` reconstructs the normalized English v1.1 baseline from the Japanese ROM; `src/corrections.json` is the cumulative, checked repair recipe. `qa26/adjustments.json` is the editable source for the latest text distribution corrections. Earlier editable translation and asset sources, insertion scripts, address maps, legacy patch history, and the user's title assets remain in their original `qa*/`, `assets/`, `formats/`, `localization/` and `docs/history/` directories. The [original translation and its credits](docs/UPSTREAM_TRANSLATION.md) are documented separately. The project does not claim to contain the game's original source code.

For a separate semantic rebuild, set `CONTINUITY_INPUT_JP` to the absolute private Japanese ROM path for both `python3 qa26/release_build.py` and `python3 qa26/verify_scope.py`. These steps check the active edits against the immutable HF19 recipe and review the recorded HF20 native runs. Do not edit `src/corrections.json` alone without regenerating and validating the corresponding semantic changes.

## What changed and how it was checked

- [Latest HF20 HTML visual comparison](QA26_HF20_Correccion_Estetica.html): 14 text resources improved, six line reflows, twelve excess blank cells removed; Astra and the coordinator visually reviewed all 18 paired pages. Native font and code remain intact.
- [HF19 full linguistic and visual report](docs/reports/QA24_HF19_Informe_Consolidado_V1-V5.html), [QA25 spacing audit](docs/reports/QA25_HF19_Auditoria_Distribucion_Texto.html), and [earlier reports](docs/EVIDENCE_INDEX.md) record their original scope and provenance.
- [HF20 save and gameplay regression HTML](QA27_HF20_Guardado_y_Regresion.html): eight paired native sessions comparing HF19 and HF20, 89 checks, identical protected 32 KiB saves and 56 identical captures in the tested scenarios. The complete QA27 run bundle is in [`support/`](support/).
- [Confirmed original Japanese ROM fixes and limitations](docs/ORIGINAL_ROM_FIXES.md) distinguish technical repairs from reported incidents that were not reproduced.
- [HF1 through HF20 history](docs/HISTORY_HF1_HF20.md) and [active validation scope](docs/RELEASE_STATUS.md) document what remains open.

The current QA26 sessions remain browsable under `evidence/qa26_runs/`. Earlier controlled native traces and fixtures are preserved with their paths in [`support/historical_native_evidence.zip`](support/historical_native_evidence.zip); extract them using `python3 tools/restore_historical_evidence.py --to restored` when needed. The full formal QA26 snapshot held 115,444 files and 6.8 GB of evidence; this repository is a documented subset of that raw evidence, while preserving all build inputs. See [source provenance](docs/SOURCE_PROVENANCE.md) and [repository notes](docs/GITHUB_PUBLISHING.md). Verify the tracked export with `python3 tools/verify_github_export.py .` before generating build files.

## Credits and redistribution

The English v1.1 translation on which this cumulative work is based is credited to **SpecialAgentApe** (hacking, menu translation, graphics editing) and **Higsby** (translation), with **ShinxHijinx** (testing) and **wowjinxy** (special thanks), as listed in the included original readme. [Original translation listing on Romhacking.net](https://www.romhacking.net/translations/5525/) · [source and credit details](docs/UPSTREAM_TRANSLATION.md).

This is a fan translation and ROM repair project. The original game and its content belong to their respective rightsholders. The provided BPS requires a separately obtained original Japanese game. The included reference BPS code retains its own license in `tools/reference_bps/LICENSE.txt`; no blanket license to the original game's content is implied. User-supplied English title artwork and the edit history have separate provenance in `assets/title/` and the phase reports.
