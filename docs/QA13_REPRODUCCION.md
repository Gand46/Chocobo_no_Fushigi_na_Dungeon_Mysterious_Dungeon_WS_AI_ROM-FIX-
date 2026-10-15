# QA13: reproducción y alcance

Mesen usado: SHA256 ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41. ROM HF9: manifest.json. No se incluyen emulador/ROM. Usar una copia de SRAM y un perfil aislado por proceso. Los comandos siguientes se ejecutan desde la raíz del paquete; cada salida debe ser nueva.

## Evidencias sin emulador

`python3 qa13/verify_scope.py --runs evidence/qa13_runs --out qa13/revalidation.json`

122 comprobaciones, incluyendo metadatos y resultados de juego. No confundir este número con122 recorridos ni con revisión global. Las capturas se revisaron directamente y la lámina sólo recorta el pie del emulador y escala los píxeles al doble, sin redibujarlos.

## Ejemplos de ejecución

```sh
python3 build.py /ruta/JP.ws --out /ruta/build
python3 qa13/equipment_sorted/run_suite.py /ruta/build/Chocobo_EN_v1.1_HF9_TEST.ws evidence/qa13_fixtures/dungeon_baseline.mss out_equipment --mesen /ruta/perfil/Mesen --suite equipment --timeout 60
python3 qa13/run.py /ruta/build/Chocobo_EN_v1.1_HF9_TEST.ws evidence/qa13_fixtures/d2_preboss.mss qa13/atla_stress.lua out_atla --mesen /ruta/perfil/Mesen --timeout 40
python3 qa13/run.py /ruta/build/Chocobo_EN_v1.1_HF9_TEST.ws - qa13/cold_event_trace.lua out_cold99 --mesen /ruta/perfil/Mesen --timeout 40 --input-save evidence/qa13_fixtures/D3_to_99_coherent_digits.sav
python3 qa13/run.py /ruta/build/Chocobo_EN_v1.1_HF9_TEST.ws out_cold99/checkpoint.mss qa13/telep_use.lua out_telep --mesen /ruta/perfil/Mesen --timeout 40
TARGET_FLOOR=30 python3 qa13/run.py /ruta/build/Chocobo_EN_v1.1_HF9_TEST.ws out_telep/checkpoint.mss qa13/elevator_caller.lua out_elevator30 --mesen /ruta/perfil/Mesen --timeout 40
python3 qa13/run.py /ruta/build/Chocobo_EN_v1.1_HF9_TEST.ws out_elevator30/checkpoint.mss qa13/save_caller_trace.lua out_save30 --mesen /ruta/perfil/Mesen --timeout 40
python3 qa13/run.py /ruta/build/Chocobo_EN_v1.1_HF9_TEST.ws - qa13/cold_event_trace.lua out_cold31 --mesen /ruta/perfil/Mesen --timeout 40 --input-save out_save30/native_save_after.sav
```

Repetir la entrada del ascensor con TARGET_FLOOR32/99 sólo cuando se necesite verificar un cambio nuevo. Los ensayos entregados ya los cubren. El control causal JP sustituye únicamente ROM y plan: elevator_causal_trace.lua reproduce el mapaA216 en30; elevator_cache_at_consumer.lua lo corrige a0000 mediante caché en RAM. Reutilizar el mismo checkpoint posterior a Telep. No interpretar elevator_cache_counterfactual.lua (escritura demasiado temprana) como un control exitoso.

El ascensor se inicia inyectando su contexto completo y el temporal de destino; la acción, mapa y retorno posteriores son nativos. Guardar se inicia mediante el guion de escalera1950; no se alcanzó esa escalera andando. Los comentarios viejos del plan capturado de Atla decían «no memory writes»: el cuerpo muestra la inyección de HP/bolsa, siempre documentada; la cabecera de la fuente reutilizable ya está corregida. El campo method de las corridas de equipamiento heredaba «single bag record»; el cuerpo, casos y capturas prueban bolsa18. La etiqueta del lanzador reutilizable se corrigió. Las copias ejecutadas y sus hashes se preservaron sin editarlos.

QA13_RUN_INDEX.json enlaza cada entrada por SHA256 a su fixture o checkpoint incluido, registra parámetros y separa los9 intentos descartados/diagnósticos de la evidencia aceptada. Un intento fallido del observador no es un bloqueo de la ROM. Los timeouts son límites del harness, no pruebas del fallo histórico.

Atla tiene HP1 y bolsa completa antes del rescate. d2_boss_assist.lua bajaHP del jefe y mantieneHP del jugador: combate asistido explícito. ending_progress.lua y post_ending_walk.lua continúan por botones. Ver límites en INFORME_ES.md.
