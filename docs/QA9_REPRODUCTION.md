# QA9: reproducción y alcance

Mesen 2.1.1 Linux x86_64, SHA256 ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41. Driver aadce17bdbcbd0801c2d4d7c86eb240bce6958305303c6d140e3818655257074. No se distribuye el ejecutable ni ROM/BIOS. Usar un perfil independiente por proceso. Python3; GNU as/ld para reconstruir el nuevo ensamblador. Los comandos siguientes parten de la raíz de fuentes.

## Build y ensamblador

```sh
python3 build.py /ruta/JP.ws --out build
as --32 src/floor_digits.s -o /tmp/chocobo_floor.o
ld -m elf_i386 -e floor_digits_guard -Ttext 0 --oformat binary /tmp/chocobo_floor.o -o /tmp/chocobo_floor.bin
```

Los 50 bytes desde FDA8 del binario ensamblado deben coincidir con `FLOOR_DIGITS_READ_GUARD` de src/corrections.json. El salto de14D398 sustituye la llamada aE1BC; el stub ejecuta esa llamada, conserva flags y registros, restringe banco/puntero/dirección y vuelve aD39B. El acceso especial usa la rutina original6E1C. No se modifica SRAM persistente adicional; solo se actualiza la caché de cinco dígitos existente.

## Matriz de carga fría

```sh
python3 qa9/run.py build/Chocobo_EN_v1.1_HF6_TEST.ws - qa9/cold_event_trace.lua out99 --mesen /ruta/perfil/Mesen --input-save qa8/event_fixtures/D3_post_ending_to_99.sav --timeout 25
```

Repetir con qa9/event_fixtures/D3_to_N.sav para los otros destinos. F98 utiliza qa8/event_fixtures/D3_post_ending_to_98.sav. Cada fixture conserva su hash; modifica campos de destino en un bloque de progreso obtenido después del final sintético. La caché61 queda deliberadamente desactualizada. `D3_to_99_coherent_digits.sav` es el control con caché98: HF5 ya lo carga correctamente.

`cold_event_trace.lua` depende de qa6/load_data_trace.lua y qa3/cold_verified.lua. Registra las dos copias de payload, escrituras de piso/flags y hasta300 opcodes del intervalo de selección. Los campos de sram.bin son SRAM viva; el bloque6BD8..75AB debe igualar75B6..7F89 en cada instantánea load_*_copied.sav. No confundir igualdad de carga con integridad retrospectiva de una partida legacy.

```sh
python3 qa9/verify_qa9.py /ruta/HF5.ws build/Chocobo_EN_v1.1_HF6_TEST.ws evidence/qa9_runs --out verificacion.json
```

Comprueba53 offsets cambiados, checksum, destinos, flags y copia exacta. Las capturas confirman que se alcanza una escena; no prueban todos los eventos o combates de cada piso. F77 no selecciona evento especial en esta tabla nativa.

## Telep y reentrada

Estado inicial de F99: evidence/qa9_runs/q9_fixed99/checkpoint.mss, procedente de la primera candidata. El script qa9/telep_use.lua inyecta únicamente la ficha de carta {cantidad1, ID0B, nivel0, aux0, flags0}, abre el inventario y ejecuta Use. q9_telep99 documenta el retorno al pueblo con la caché99 conservada.

`qa9/event_fixtures/post_telep99_reentry30.json` documenta la preparación exacta: copia el bloque vivo posterior a Telep a un contenedor de guardado legacy y cambia D3, piso29 y máximo29. Se preservan progreso, caché y demás datos. El cargador nativo incrementa hasta30. q9_hf5_telep_reentry30 termina con7335=A217; q9_hf6_telep_reentry30 con7335=0000. Se registran capturas y una secuencia posterior de movimiento.

Clasificación: salida nativa desde acceso sintético + reentrada sintética mediante SRAM + carga nativa. No es la ruta continua del ascensor. Los intentos q9_*entry*, q9_*active* y q9_*elevator* son diagnósticos incompletos, excluidos del PASS. El menú E0:2873 usa060E como selección y7558/7559 como temporales; aún falta reproducir su llamador completo. El gancho final se restringe a selectores E1 para no interferir con esas variables temporales.

## Guardado coherente

q9_stair_prompt98 reubica el tile de escalera031D inmediatamente encima del personaje en el mapa de F98. q9_native_save98 elige Save and go on mediante pulsaciones normales. Su native_save_after.sav conserva una partida protegida con piso98 y dígitos98. q9_hf5_native_cold99 y q9_hf6_native_cold99 cargan F99/A216. Es control negativo de corrupción: esta ruta nativa concreta no falla en HF5.

## Fuente y rana

Usar el checkpoint previo al final evidence/qa8_runs/q8_d2_boss_assist/checkpoint.mss, SHA25615e4575eb5ed9f4b8239e4a0ae58b26d3022e785be0804fa7ad366f87ecd9179. Mantiene la asistencia al combate documentada en QA8; no es una partida natural completa.

```sh
FOUNTAIN_FULL=1 python3 qa9/run.py build/Chocobo_EN_v1.1_HF6_TEST.ws evidence/qa8_runs/q8_d2_boss_assist/checkpoint.mss qa9/fountain_coherent.lua out_fountain --mesen /ruta/perfil/Mesen --timeout 25
```

FOUNTAIN_FULL=0 usa15 Geyser+5 Frog y máscara0090 en7313. FULL=1 usa45+15 y máscara03F0. Estos campos concuerdan con los umbrales nativos de194E8C..4F7E:15/30/45 Geyser y suma20/40/60. Son datos sintéticos coherentes, no ventas realizadas en el juego. Se mantienen flags acumulados y se pulsa A; no se salta el guion. El final llega aE0:ABE2. El control JP utiliza el mismo estado; los bloques de guion A200..ABFF y13E00..144FF son idénticos entre JP yHF5. No se infiere de estos ensayos que el testimonio del foro sea falso.

QA9_RUN_INDEX.json distingue parámetros, hashes, candidatas, resultados finales e intentos descartados. run.json conserva órdenes históricas con rutas originales; adaptar solo las rutas al reproducir. Las primeras hipótesis4D/12 eran ajenas a fuente/rana. La sonda0647=1 solo aisló el bucle y no forma parte del parche.
