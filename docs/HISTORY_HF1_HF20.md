# Cumulative patch history

Every published HF BPS targets the same Japanese ROM (CRC32 `CCAA4853`) directly. The active source and patch are HF20 TEST; older source definitions and reports are retained to explain the path, not chained during installation.

| Version | Main cumulative addition | Primary evidence |
| --- | --- | --- |
| HF1 | Ten text stream repairs, termination/conditional wording, checked JP-to-English recipe | `docs/HF1_CHANGELOG.md` |
| HF2 | Lafoss selector guard for the invalid `FF` graphics pointer | `docs/history/hf2/INFORME_ES.md` |
| HF3 | Whistle tile/map/palette repair after reproducing its residual glyph | `docs/history/hf3/INFORME_ES.md` |
| HF4 | Protected SRAM save format with CRC16, commit, legacy load and interrupted-write rejection | `docs/history/hf4_qa7/INFORME_ES.md` |
| HF5 | Lafoss projectile, native pearl damage and an additional text terminator | `docs/history/hf5_qa8/INFORME_ES.md` |
| HF6 | Event selector refreshes stale floor digits with the original converter | `docs/history/hf6_qa9/INFORME_ES.md` |
| HF7 | First English title integration and scoped title/equipment/Atla review | `docs/history/hf7_qa10/INFORME_ES.md` |
| HF8 | User-provided English title logo integrated into 139 native tiles and maps, native animation retained | `docs/history/hf8_qa11/INFORME_ES.md` |
| HF9 | Additional fixes consolidated; QA13 later validated save/equipment/Atla/elevator scenarios without changing the HF9 ROM | `docs/history/hf9_qa12/INFORME_ES.md`, `docs/history/qa13/INFORME_ES.md` |
| HF10 | Title subtitle recomposed in native 2bpp font, main user art unchanged | `docs/history/qa14/INFORME_ES.md` |
| HF11 | G05:M002 line break; scoped layout M1 | `docs/history/QA15_INFORME_ES.md` |
| HF12 | M3: eleven unique dialogue/template repairs, variable cases and credits review | `docs/history/qa17/INFORME_ES.md` |
| HF13 | M4: five bounded layout/pagination resources | `docs/history/qa18/INFORME_ES.md` |
| HF14 | V1: 36 corrected story references with verified bank allocations | `docs/reports/QA19_V1_Informe.html` |
| HF15 | V2: 74 text/presentation repairs and item terminology | `docs/reports/QA20_V2_Informe.html` |
| HF16 | V3: 64 story resources and two equipment property labels | `docs/reports/QA21_V3_Informe.html` |
| HF17 | V4: 43 G09 dialogue repairs | `docs/reports/QA22_V4_Informe.md` |
| HF18 | V5: 65 G14 labels and two Chip name reconciliations | `docs/reports/QA23_V1-V5_Informe_Consolidado.html` |
| HF19 | QA24: four story resources and two bestiary getter names; eleven earlier lexical reservations reviewed with Astra. QA25 measured distribution without changing the ROM. | `docs/reports/QA24_HF19_Informe_Consolidado_V1-V5.html`, `docs/reports/QA25_HF19_Auditoria_Distribucion_Texto.html` |
| HF20 | QA26: six reflows and twelve oversized blank cells removed in 14 resources. Native font/code kept; 28 dialogue sessions, 18 paired pages. | `QA26_HF20_Correccion_Estetica.html` |

QA27 reran native save/cold-load, equipment and assisted-combat scenarios on HF19 and HF20 without modifying ROM bytes: eight sessions, 89 checks and 56 screenshot pairs matched. See `QA27_HF20_Guardado_y_Regresion.html` and `support/`.

For every version, read the corresponding report's limitations. The project has not received universal visual/linguistic or natural-playthrough approval.
