# Chocobo English v1.1 + HF6 TEST

Incluye HF1–HF5 y la corrección de caché del piso en selectores de eventos de D3. TEST, no RC. El título continúa japonés y la aprobación global sigue pendiente.

Aplicar patches/Chocobo_EN_v1.1_HF6_TEST_JP_CCAA4853.bps directamente a JP CRC32 CCAA4853. Para reconstruir:

```sh
python3 build.py /ruta/JP.ws --out build
python3 -m unittest discover -s tests -v
python3 tools/verify_evidence.py /ruta/JP.ws
python3 tools/verify_independent_bps.py /ruta/JP.ws
```

Fuentes acumulativos reconstruidos; no incluyen ROM/BIOS. src/corrections.json fija preimágenes. src/floor_digits.s contiene el nuevo ensamblador; src/save_guard.s conserva la protección del guardado. Ejecutar las pruebas desde esta raíz.

Informe vigente: INFORME_ES.md. Procedencia y reproducción: docs/QA9_REPRODUCTION.md, QA9_RUN_INDEX.json, QA9_VERIFICATION.json. Los documentos de docs/history describen revisiones anteriores.

HF4/HF5/HF6 comparten formato de guardado. Para versiones antiguas, exportar una copia:

```sh
python3 tools/chocobo_save.py partida.sav --export-legacy copia_legacy.sav
```

Usar SRAM cruda de32 KiB; no confundirla con savestates. La protección no recupera un bloque anterior sobrescrito.

IDENTIFICACIÓN
JP SHA256: 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728
HF6 SHA256: 87ecaab08786651ee9431d6e386b0b73147e759aee282c053f6a75249e820d73
HF6 CRC32: 37109106; checksum WS: EBA8
BPS SHA256: a92cf352b84318ffb7f0c168ea7515da961cd044589500169e9db92e384be418
