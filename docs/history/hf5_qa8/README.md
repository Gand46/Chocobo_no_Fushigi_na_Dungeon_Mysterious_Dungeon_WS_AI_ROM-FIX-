# Chocobo English v1.1 + HF5 TEST

Compilación experimental, no RC. Incluye HF1–HF4 y tres fixes de QA8: proyectil Lafoss, acceso al daño nativo de las perlas FE/FF y terminador de la familia 0, entrada 81. Sigue pendiente la aprobación global. El título continúa japonés.

Aplicar patches/Chocobo_EN_v1.1_HF5_TEST_JP_CCAA4853.bps directamente a JP CCAA4853, sin parches previos. Alternativamente:

```sh
python3 build.py /ruta/JP.ws --out build
python3 -m unittest discover -s tests -v
python3 tools/verify_evidence.py /ruta/JP.ws
python3 tools/verify_independent_bps.py /ruta/JP.ws
python3 qa8/text_census.py /ruta/JP.ws build/Chocobo_EN_v1.1_HF5_TEST.ws --out census
```

El build requiere Python 3 y no incluye ROM ni BIOS. src/corrections.json conserva precondiciones exactas. Los recursos anteriores y la protección de guardado se integran acumulativamente. El ensamblador de la protección está en src/save_guard.s. Estos fuentes reconstruyen la traducción/parche, no el fuente original del juego.

HF4/HF5 comparten partidas protegidas. Para versiones anteriores, exportar una copia legacy verificada:

```sh
python3 tools/chocobo_save.py partida.sav
python3 tools/chocobo_save.py partida.sav --export-legacy copia_legacy.sav
```

Usar SRAM cruda de 32 KiB, no savestates. Las partidas legacy no tienen CRC retrospectivo. La protección rechaza un bloque incompleto; no recupera automáticamente una partida sobrescrita. Conservar una copia antes de probar esta versión TEST.

Estado vigente: INFORME_ES.md, docs/issue_register.json y docs/quality_gates.json. Reproducción QA8: docs/QA8_REPRODUCTION.md. Capturas y savestates: evidence/qa8_runs. Los documentos de docs/history describen builds anteriores y no sustituyen el estado HF5.

## Identificación exacta

JP SHA-256: 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728
HF5 SHA-256: 312f688f627f0c5ccf430c35c9632033344fc0397aa25c6f0db9d99a3630f9c8
HF5 CRC32: 3887C0CF; checksum WS: 06CA
BPS SHA-256: 1fd0c2c34329d4f1961b311ad7b6fff8403331825d71f5057795de2029fee665
