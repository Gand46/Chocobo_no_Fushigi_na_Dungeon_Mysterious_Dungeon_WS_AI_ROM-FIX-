# Chocobo English v1.1 + HF9 TEST

Corrige cuatro textos visibles: propiedad contra no muertos, ataque de tres direcciones, elemento de fuego en silla y nombre de Sleep Card. Conserva el logo aportado y todos los fixes HF1–HF8. TEST: la causa del bloqueo histórico por equipamiento no está resuelta.

Aplicar `patches/Chocobo_EN_v1.1_HF9_TEST_JP_CCAA4853.bps` directamente a la ROM japonesa original CRC32 `CCAA4853`. Sin parches intermedios. No se distribuyen ROM, BIOS ni emulador.

## Reconstruir

`python3 build.py JP.ws --out build`

Python 3, sin dependencias externas para el build. `BUILD.bat` y `BUILD.command` conservados; no probados en Windows/macOS durante QA12. Verifica base, preimágenes, rangos, checksum y hash final.

`python3 tools/verify_independent_bps.py JP.ws`

## Fuentes y pruebas

Ediciones acumulativas: `src/corrections.json`. Textos nuevos y procedencia japonesa: `localization/hf9_text_repairs.json`. Se reutiliza la fuente nativa, sin dibujar glifos ni mover punteros. Los bytes sobrantes después del nuevo terminador de tres direcciones son inalcanzables; el slot siguiente queda intacto.

Pruebas portables y comandos: `docs/QA12_METODO_Y_LIMITES.md`. Evidencia de esta fase: `evidence/qa12_runs/`. Las pruebas históricas mantienen sus hashes y no se presentan como nuevas ejecuciones de HF9. `docs/issue_register.json` es la lista vigente de pendientes.

Logo vigente: `assets/title/user_v01`; importador `tools/integrate_title_assets.py`; integración documentada en `docs/QA11_INTEGRACION_LOGO.md`. No volver al rótulo provisional HF7.

Consultar `INFORME_ES.md`, `manifest.json`, `docs/quality_gates.json` y `CONTEXTO_CONTINUACION.md`.
