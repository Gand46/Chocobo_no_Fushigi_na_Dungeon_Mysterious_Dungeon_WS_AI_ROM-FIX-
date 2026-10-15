# Reproducción QA15 / M1

1. Construir desde la ROM japonesa verificada: `python3 build.py JP.ws --out build`.
2. Verificar parche y alcance: `python3 tools/verify_independent_bps.py JP.ws` y `python3 qa15/verify_scope.py --japanese-rom JP.ws --out validation.json`.
3. Regenerar censo: `python3 qa15/inventory_layout.py --rom build/Chocobo_EN_v1.1_HF11_TEST.ws --label HF11 --jp JP.ws --out census`.
4. En Linux, Mesen debe tener el hash del manifiesto y `settings.json` con `{}` junto al ejecutable. El ejecutable no se distribuye. Para repetir el caso final, establecer `LAYOUT_OBSERVER` a la ruta absoluta de `qa15/layout_observer.lua` y ejecutar `python3 qa15/run.py build/Chocobo_EN_v1.1_HF11_TEST.ws evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss qa15/dialogue_go_final.lua salida_nueva --mesen /ruta/Mesen --timeout 15`.

El checkpoint procede de una ruta anterior asistida. El plan sustituye una vez grupo/mensaje por5/2 cuando el motor va a iniciar el siguiente diálogo. Es `SAVESTATE + POINTER_INJECTION`; no demuestra obtención ni recorrido natural. El texto y los píxeles los produce la ROM nativa. El controlador pulsaA en50 y350; completa500 cuadros. Comprobar salida0, completed.txt, ausencia de dump_error.txt y los hashes de run.json. No ejecutar varios procesos sobre el mismo perfil a la vez.

El caso final registra0106 en línea1/columna0 y cero auto_line; el control HF10 lo registra como auto_line en columna13. Capturas nativas en150/300/420; el contacto amplía por vecino más próximo. La lectura visual está documentada aparte, no deducida sólo del código.

Los registros de cada ejecución guardan el observador exacto y su hash en provenance.json. Las primeras tres usanv1; las restantesv2. Los ensayos sin lecturas narrativas aportan como máximo ventanas/menús, no cobertura de diálogos. El intento hf11_dialogue_go terminó por timeout y queda como diagnóstico. El PASS procede exclusivamente de hf11_dialogue_final.

No es necesario repetir QA13 funcional o QA14 logo para este cambio: los seis bytes modificados pertenecen al recurso de texto especificado. El verificador histórico QA14 consulta su manifiesto y parche fijados en docs/history/qa14 y patches/historical.
