# Continuidad HF4 TEST / QA7

Última ROM identificada: SHA256 1ec449933e812c8e4f5e83b882db17b4c5f1ce3b5ea85527d9a1dd2a0891060d; CRC32 12E75051; checksum06C5. Base JP SHA256 38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728. Estado experimental, no RC.

SAVE-01: aceptación de escritura parcial corregida; no recuperación ni causa natural demostrada. Ver informe, formato y matrices. No repetir matrices descartadas DS=0 ni confundir «completed» con resultados. Usar tools/chocobo_save.py para HF4; el analizador QA6 histórico no reconoce el nuevo formato.

Siguiente trabajo: cerrar EN-02 identificando el recurso ausente FFFF y semántica real; o avanzar JP-02 desde evidence/qa7_runs/q7_d2_dialogue_progress/checkpoint.mss, procedencia HF4 sobre fixture D2 sintética. Todavía no es el segundo final. D2 usa flag0080 de palabra730A, no8000. D3 añade730C bit4. Conservar la distinción entre ruta sintética y adquisición natural.

No reabrir el fallo eléctrico del cartucho. No introducir cambios especulativos en JP-01/03/04 sin consumidores/rutas y precondiciones. TR-01 global y TR-03 siguen abiertos. Evidencias HF1–HF3 conservadas; los seis nuevos rangos solo afectan guardado. Mantener BPS acumulativo desde JP y fuentes completos.
