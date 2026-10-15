# Original Japanese ROM issues: verified changes and unresolved reports

This page distinguishes defects in the Japanese game, problems introduced or exposed by the English translation, and historical user reports. A synthetic PASS means native code was executed in an identified controlled state; it is not a claim that the reported natural trigger has been reproduced.

| ID / release | Observed cause and intervention | Evidence and scope |
| --- | --- | --- |
| `JP-01`, `JP-03` / HF6 | The authoritative floor at SRAM `7303` and cached decimal digits at `753A..753E` can disagree. A D3 event selector consuming the stale digits chose the special F99 map while entering F30 after Telep. HF6 refreshes those digits with the game's original conversion routine at the event consumer (`14D398` hook; new code `14FDA8..14FDD9`). | Reproduced the wrong map selection in the Japanese ROM after a controlled Telep/return chain. With the consumer cache refreshed, JP selects ordinary map `0000` instead of the wrong special event. Native save and cold load also passed. The precise later freeze described online was **not** reproduced, and natural access to every path was not demonstrated. [HF6 investigation](history/hf6_qa9/INFORME_ES.md); [QA13 linked scenarios](history/qa13/INFORME_ES.md). |
| `SAVE-01` / HF4 | The inherited save format could accept a partially written shared block. HF4 invalidates old markers before writing, adds a CRC16, complement and final commit marker, and checks them on load. Six SRAM bytes at `7F8A..7F8F` are reserved. | Interruption matrices over 2,534/2,538 write prefixes rejected mixed protected payloads; new saves and legacy load passed. A protected save cannot restore data already overwritten; the exact historical natural reset remains unknown. [HF4 save report](history/hf4_qa7/INFORME_ES.md); [QA13](history/qa13/INFORME_ES.md). HF20's [QA27 regression](../QA27_HF20_Guardado_y_Regresion.html) produced the same valid 32 KiB save as HF19 and reloaded two exact 2,516-byte copies. |
| `TR-02` / HF3 | Japanese whistle rendering loaded 37 tiles but its map used tile 38 in 18 cells, leaving a previous menu glyph visible. The glyph's appearance changed with translation. HF3 added three native palette tiles and adjusted map pointers without changing executable code or fonts. | 2,399 native frames compared, 18 repaired cells traced; use and return to play passed. [HF3 whistle report](history/hf3/INFORME_ES.md). This is a graphical defect observed in JP, amplified by English text. |
| `EN-02` / HF2 and HF5 | Lafoss ID `FF` had no valid selector entry and produced a `FFFF` graphics pointer, causing a loop when using its native menu entry; observed in Japanese and English states. HF2 guards this selector. HF5 repairs native projectile/damage dispatch for IDs `FE/FF`. | Scoped native use, damage and enemy death tests passed. Natural acquisition and the full original animation/effect remain unproven. [HF2](history/hf2/INFORME_ES.md); [HF5](history/hf5_qa8/INFORME_ES.md). |

## Reports investigated without a speculative binary fix

| ID | Established outcome |
| --- | --- |
| `JP-02`, fountain/frogs | Two coherent configurations before the ending completed in JP and repaired builds. The reported failure was not reproduced; no frog-specific binary patch was added. |
| `EN-01`, full bag and equipment | Multiple native synthetic cases, including a full fused bag, returned to the field without observed protected-save writes. The historical trigger and cause remain unknown. QA27's six HF19/HF20 paired equipment cases match byte for byte. |
| `JP-04`, Atla rescue | A full-bag/low-HP controlled route passed the rescue and a subsequent assisted boss/ending chain. The original report's exact failure state remains unknown; no speculative Atla patch was added. |
| Cartridge electrical failure | The user established an electrical issue on physical hardware. It is outside ROM patch scope. |

English text repairs, title translation and font-aware layout changes are documented in [the version history](HISTORY_HF1_HF20.md). The labels above do not assert a complete natural playthrough, hardware approval or global absence of defects.
