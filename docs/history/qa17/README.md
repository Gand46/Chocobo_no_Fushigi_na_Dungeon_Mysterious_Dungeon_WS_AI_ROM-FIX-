# Chocobo English HF12 TEST — QA17 / M3

Fuentes acumulativas editables y parche BPS directo desde la ROM japonesa de WonderSwan. Sin ROM completa, BIOS ni emulador.

Base: 2 MiB, CRC32 CCAA4853, SHA-256 `38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728`.
Salida HF12: SHA-256 `ffb5561da6e9f15df0bdd3e028fe78b19f05a79916f88cc5503ea25216bfe3d1`, CRC32 `58CEAE7E`, checksum `FA41`.

Aplicar `patches/Chocobo_EN_v1.1_HF12_TEST_JP_CCAA4853.bps` a una copia limpia de la ROM japonesa, no a HF11. La aplicación del parche debe verificar la base.

Reconstruir y comprobar con Python 3 desde esta carpeta:

```sh
python3 build.py "/ruta/original-japonesa.ws" --out "/ruta/salida-nueva"
python3 qa17/verify_scope.py --japanese-rom "/ruta/original-japonesa.ws" --out "/ruta/validacion-qa17.json"
```

`src/legacy_translation_ranges.json` reconstruye la traducción previa; `src/corrections.json` contiene todas las correcciones acumulativas con precondiciones. `build.py` comprueba hashes, límites, checksum y BPS. No se requiere ejecutar los scripts de experimentación con rutas del entorno original para reconstruir la versión.

Los verificadores QA15 y QA16 se fijaron explícitamente al BPS histórico HF11 conservado. Sus comprobaciones archivadas pasan y no se presentan como nuevas sesiones HF12. La validación actual es QA17. `evidence/qa17_runs/*/provenance.json` conserva la ruta y hash del checkpoint, la inyección y el observador. `qa17/run.py` requiere un Mesen compatible con Lua; el binario usado está identificado por SHA en manifest.json.

29 PASS_SYNTHETIC acotados. 11 recursos únicos corregidos, 14 casos de variables y 14 pantallas de créditos. M3 de 4 ejecutada; maquetación y fidelidad lingüística global siguen abiertas. Leer INFORME_ES.md y CONTEXTO_CONTINUACION.md antes de continuar.
