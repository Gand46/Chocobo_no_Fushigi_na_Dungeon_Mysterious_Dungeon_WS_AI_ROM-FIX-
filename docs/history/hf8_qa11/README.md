# Chocobo English v1.1 + HF8 TEST

Integra el logo inglés aportado por el usuario y conserva todas las correcciones de HF1–HF7. Versión TEST, no RC ni aprobación global.

Aplicar `patches/Chocobo_EN_v1.1_HF8_TEST_JP_CCAA4853.bps` directamente a la ROM japonesa original CRC32 `CCAA4853`. No requiere parches intermedios. La ROM, BIOS y emulador no se distribuyen.

## Reconstruir

`python3 build.py JP.ws --out build`

Python 3 sin dependencias externas para el build normal. En Windows: `BUILD.bat "C:\ruta\JP.ws"`; lanzador conservado, no probado en Windows durante QA11. El build verifica la base, preimágenes, rangos, checksum y hash de la versión publicada.

## Editar el nuevo logo

Fuentes canónicas: `assets/title/user_v01/assets/`, su `layout.json` y `tools/build.py`. Se conserva el paquete gráfico aportado, incluidos sus maestros y referencias. El README interno describe su estado offline v0.1; la integración vigente se documenta en `docs/QA11_INTEGRACION_LOGO.md`.

Con Pillow y NumPy instalados:

`python3 tools/integrate_title_assets.py JP.ws --out title_edits.json --report title_report.json --write-source`

El importador recompone los recursos desde los PNG editables, convierte mapas y patrones, comprueba el espacio asignado y reemplaza únicamente las entradas `TITLE_` de `src/corrections.json`. A continuación usar `build.py --development` para una edición intencional; verificarla antes de actualizar el hash de publicación. El generador `generate_title_fix.py` es histórico de HF7 y no representa el logo actual.

Consultar `INFORME_ES.md`, `manifest.json`, `docs/QA11_RUN_INDEX.json`, `docs/approval_matrix.json` y `CONTEXTO_CONTINUACION.md`. Los pendientes anteriores se mantienen en `docs/issue_register.json`.
