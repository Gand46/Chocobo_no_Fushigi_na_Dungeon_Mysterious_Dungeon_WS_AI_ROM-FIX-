# QA16 · Reproducción y límites

UsarMesen2.1.1 SHA256ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41. Un solo proceso por perfil, settings.json={} junto alejecutable. No es necesarioXvfb. Driver yobservador quedan fijados por hash. Cargar laROM HF11 reconstruida, nunca distribuirla.

```sh
LAYOUT_OBSERVER="$PWD/evidence/qa16_runs/shop_buy_purchase/observer.lua" python3 qa16/run.py /ruta/HF11.ws evidence/qa16_runs/shop_enter/checkpoint.mss qa16/shop_buy_purchase.lua /ruta/salida --mesen /ruta/Mesen --timeout 15
python3 qa16/verify_scope.py --japanese-rom /ruta/JP.ws --out /ruta/QA16_VERIFICATION.json
```

Cada provenance.json da state_path ytipo de acceso. SAVESTATE siempre; WRAM_POKE parafixtures SRAM; POINTER_INJECTION para guion/selector sintético. Observarplan.lua para todas las escrituras. El comando usa un escenario concreto, no un recorrido natural. Un proceso terminado no otorgaPASS: verificar transacción, getters, selección real, imágenes, integridad y ausencia de dump_error.

stores.csv registra los stores comunes7AFF/7B7D/7BC1/7BFD/7B5A, no todas las escrituras ni las rutinas numéricas. Ancho:rel_byte*4px, avance2bytes para8000h y4para glifo normal. Se compara con ancho interior del preset; los resultados visuales corresponden a capturas identificadas envisual_readings.json. No se usaOCR. La revisión fue con contexto, no ciega ni independiente.

shop_default tuvo timeout yqueda excluido. status_long_plus/minus son intentos ineficaces. window49 no esfixtureválido. storage_tail fuerza contexto aún no encontrado: cinco stores exceden el ancho de suventana, noelbuffer52bytes. No cambiarF00:I053 con esa única prueba. Se mantienen13 alertasde M1 sin afirmar13fallos.

QA16 final: `magic_display99` sustituye al ensayo `magic_boundaries` en la lista de PASS. Los valores 99 se muestran completos (Lv.99, ATB99 y NEXT99P). El ensayo anterior con 255 se conserva como diagnóstico excluido porque supera el formato de dos cifras. No demuestra un defecto alcanzable de la ROM.
