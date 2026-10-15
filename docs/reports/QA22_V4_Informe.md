# Chocobo English HF17 — validación visual y lingüística V4 (4 de 5)

**Dictamen:** V4 ejecutada con aprobación visual sintética acotada de las 194 referencias G09. La revisión lingüística acotada aprueba 192; dos conservan una reserva de grafía. La aprobación global del juego continúa pendiente de V5 y de las reservas heredadas.

| Ámbito | Resultado comprobado |
|---|---|
| Corpus G09 | 194 referencias de `qa19/five_validation_plan.json`; cotejo visual con texto japonés y base HF16 en 33 láminas `qa22/audit_*.png`. |
| Correcciones | 43 diálogos bilingües corregidos; 17 caben in situ y 26 se relocalizan dentro del mismo banco 06. Se conserva la tabla G09 de 256 entradas. |
| Capturas finales | 194 selecciones sintéticas en Mesen; 47.451 cuadros, 221 imágenes de página y 194 terminadores observados. Cero glifos no blancos descartados. |
| Herencia visual | Las 151 referencias sin edición reproducen exactamente los píxeles de página de la base HF16. Las 43 editadas se leyeron en cinco láminas `qa22/verified_changed_*.png`. |
| Reserva nueva | `G09:M086` y `G09:M089`: el japonés nombra a ドル君. Se corrige la atribución errónea a Chip; **Doru** es transliteración provisional hasta confirmar la grafía inglesa establecida. |
| Integridad | 1.483 comprobaciones de alcance; 13 pruebas unitarias; BPS directo de la ROM japonesa con aplicación independiente exacta; regeneración editable exacta desde JP+historial+43 ediciones. |

Las correcciones recuperan instrucciones de libros, Talons/Saddle, fusión, bolsa y regreso a la aldea. El tramo final distingue que la voz es una petición de auxilio, que puede viajar entre calabozo y superficie pero no luchar, y que **Atla pide al chocobo que lo rescate** (`G09:M186–192`). Se revisó la paginación de mensajes largos para que las frases clave se completen en la ventana y los cambios se leen en capturas reales del motor.

La ROM HF17 tiene SHA-256 `951c3bb6b7ddc2d8685c8b9d5160fffcee6fffbc0fe6bb72c3a91c29c3e88d0f`, CRC32 `8E66BB8E` y checksum WonderSwan `2C5E`. El parche `patches/Chocobo_EN_v1.1_HF17_TEST_JP_CCAA4853.bps` tiene SHA-256 `4fef3b88991d6b47be0b89615d7f9a4767f1016238913db0da39b6f067d3ba8f`; se aplica directamente a la ROM japonesa limpia CRC32 `CCAA4853`, SHA-256 `38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728`. El ZIP de fuentes no contiene la ROM comercial.

Evidencia y reproducción: `qa22/translations.json`, `qa22/linguistic_review.json`, `qa22/visual_readings.json`, `qa22/verification.json`, `qa22/rebuild_translation_edits.py`, `qa22/verify_scope.py` y `evidence/qa22_runs/verified_*`. Los prefijos `baseline_` y `candidate_` son diagnósticos anteriores; **sólo `verified_` corresponde a HF17 final**. El verificador valida el SHA de la ROM de cada sesión, el savestate, emulador, driver y plan. La región libre se comprobó desde `06:F708`; el último nuevo byte llega antes de `06:FCA0`. No se editó la fuente de glifos compartida.

Quedan V5: 154 referencias G14, créditos, gráficos/título, coherencia terminológica transversal y las reservas V2 (`G00:M252–255`, `G04:M033–034`), V3 (`G06:M100`, `G11:M011`) y heredadas (`G16:M073`, preset32/F00:I053, consumidores `G16:M000/M003/M004`). Estas pruebas son selecciones sintéticas de texto; no certifican todo el recorrido natural, hardware, segundo emulador ni segunda revisión independiente.
