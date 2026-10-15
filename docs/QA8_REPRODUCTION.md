# QA8: reproducción, procedencia y límites

Entorno ejecutado: Linux x86_64, Mesen2.1.1 SHA256 ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41. Driver aadce17bdbcbd0801c2d4d7c86eb240bce6958305303c6d140e3818655257074. Perfiles portables independientes; no ejecutar dos procesos en el mismo perfil. El emulador proviene del insumo del usuario y no se redistribuye. Python3 y Pillow para verificadores de imagen; el build no requiere Pillow.

QA8_RUN_INDEX.json registra hash de ROM/estado y parámetros. run.json conserva la orden original y sus rutas históricas, no portables. plan.lua conserva el plan principal. QA8_SCRIPT_HASHES.json fija las dependencias Lua/Python de este paquete. Los estados no contienen la ROM y necesitan el build indicado o compatibilidad justificada. HF5 difiere de HF4 en los siete offsets de qa8_static_fix_scope.json; los eventos y guardado no cambian. Las primeras sondas Lafoss usan una candidata con el proyectil, otras añaden daño, y la final incorpora también el texto. Sus hashes quedan separados.

## Comandos desde la raíz del paquete

Primero construir HF5 con build.py y suministrar el ejecutable de Mesen. Elegir carpetas de salida nuevas. Ejemplo de la ruta Lafoss en la revisión final:

```sh
python3 qa8/run.py build/Chocobo_EN_v1.1_HF5_TEST.ws evidence/qa3/q3_dungeon/checkpoint.mss qa8/damage_probe.lua out_lafoss --mesen /ruta/perfil/Mesen --timeout 25
```

La ubicación del estado q3_dungeon se puede localizar dentro de evidence si su carpeta histórica difiere; el hash esperado es 2cb9e29b3749ce0caf9628ff93f8c5b52ebe5eb7212627175290a38d9adb5f82. Es un estado anterior compartido, no una partida obtenida naturalmente con Lafoss. Se inyecta una ficha de bolsa {cantidad1,IDFF,nivel0,aux0,flags0}; el juego realiza Kick, colisión y consumo. ITEM_ID=254 prueba FE. Con qa8/damage_defense.lua y ENEMY_DEFENSE=200 o2000 se fija explícitamente la defensa del enemigo1. Los valores y HP de qa8/verify_fixes.py se leen de daño/instantáneas reales.

ADVERTENCIA DE TRAZA HISTÓRICA: magic_dispatch.txt contiene un campo hp procedente de58E3 que no es el HP del enemigo; no se utiliza para aprobar el efecto. La dirección verificada es5A32+2*índice. Para enemigo1:5A34. damage.txt y las instantáneas660/810 son las evidencias válidas. Los nombres filanes de algunas carpetas son etiquetas de ensayo para IDFE, no una aprobación lingüística de ese nombre.

Texto: qa8/text_suite/run_suite.py ROM ESTADO OUT --mesen EJECUTABLE --suite resources --timeout 25. El caso family0/index81 se reproduce inyectando su recurso en el consumidor nativo de descripción; es POINTER_INJECTION, no acceso natural a la etiqueta. Se leen16E6F4,16E6F6,16E6F8 y16E6FA, sin tocar16E6FC. El censo puede repetirse con qa8/text_census.py JP.ws HF5.ws --out census; el límite de cada entrada se infiere del siguiente puntero distinto y las entradas finales se acotan a512bytes. No afirma que todas las cadenas del juego estén en esas19familias. El rótulo HF5 de columnas del censo identifica la entrada traducida, que en census_before es HF4 según su hash.

Equipamiento: qa8/expanded_equipment.lua con EQUIP_ID/EQUIP_SLOT. La selección correcta se aprobó mirando selection1180.png:65 slot0 TanTalon+99;9D slot17 TanSaddle+99;BF slot17 CounterMail+99;C0 slot17 Life+99. Son acciones Check sobre una bolsa sintética de18objetos. El intento93 slot9 se excluye porque abrió TanTalon. buffer_guard solo cubre los consumidores37AFF/37B7D conDI>=23C; ausencia de hits no prueba toda la memoria.

Guardado final: qa7/save_trace.lua con SAVE_FIXTURE absoluta al generation_B.sav de q7_save_final_native, SAVE_LEVEL=3 y SAVE_HP=28; estado q3_save_prompt_fixed, hash6f0f5f7ac32b807c3ca8d2abd63a7cd13bd247d63db9d5fab93409628cc75dd4. Salida q8_save_final. Iniciar proceso nuevo sin savestate: qa8/run.py ROM - qa6/load_data_trace.lua OUT --input-save q8_save_final/generation_B.sav --mesen EJECUTABLE --timeout 25. Se verifican ambos load_*_copied.sav:6BD8..75AB igual75B6..7F89. El intento q8_save_normal carecía de fixture válida: no se considera evidencia.

## Cadena del segundo final

q7_d2_dialogue_progress -> q8_d2_event_progress -> q8_d2_event_progress2 -> q8_d2_boss_assist -> q8_d2_ending_progress -> q8_d2_return_control -> q8_d2_walk. Todos los hashes de estados sucesivos figuran en el índice. event_progress/ending_progress envían pulsos A. boss_assist fija HP del jefe5A32=1, HP/máximo del personaje500 y mantiene HP500 cada60cuadros. Tras derrotarlo, el evento avanza sin redirigir su puntero. Los créditos se ven en ending_progress/f03000; pueblo en f06000/f06600; final de guion E0:ABE2. post_ending_walk verifica desplazamiento con izquierda/derecha. Clasificación SYNTHETIC_STATE + WRAM_POKE/FREEZE (memoria SRAM viva del juego) + entradas nativas; nunca NATURAL desde partida nueva.

Fuente/rana: pendientes los flags y la bifurcación del evento. La identificación visual de cartas no acredita completar la misión: Frog04, Geyser09, Telep0B. No se aplicó un fix especulativo a la escena.

## Pisos y Atla

Fixtures mínimas D3: saved730A bit0080, saved730C bit4, saved7301=3, piso destino-1 en7303/7305; campos guardados desplazados09DE. Consultar cada JSON. Las primeras fixtures provenían del guardado temprano QA5 y no contienen todo el progreso. D3a22/66/88/99/100 quedó blanco;11/33/44/55/77 cargó una escena;30/98 podía volver al pueblo. Esto no define un catálogo universal de pisos rotos.

El control JP con la fixture mínima99 queda blanco. load_*_copied.sav distingue copia íntegra de bloqueo de reconstrucción. Las fixtures post_ending copian el bloque vivo después de la cadena de final, crean cabecera normal legacy y cambian D3/destino.98 y30 cargan campo;99 permanece blanco. q8_D3_stair_attempt y q8_D3_enter99 son intentos de movimiento: no alcanzaron99, por lo que no validan el ascensor ni Telep99→30. Conservar el checkpoint de98 para localizar correctamente la transición.

La secuencia D1 q8_D1_to_30 -> q8_D1_boss_intro -> q8_D1_ending_progress terminó en pueblo. No se identificó como el rescate de Atla; JP04 sigue NOT_VALIDATED. Se necesita un estado previo a ese rescate preciso.

## Verificación acotada y entrega

```sh
python3 qa8/verify_fixes.py /ruta/HF4.ws /ruta/HF5.ws evidence/qa8_runs --out verificacion.json
```

Compara siete offsets exactos,256resultados del selector,65536predicados del límite, trazas de daño, HP10→0, consumo,4/5palabras de texto, píxeles idénticos y cargas exactas. Las enumeraciones del selector/límite son análisis estático, no ejecución CPU de todos los casos. Las funciones reales sí se ejecutaron en las trazas de Mesen. Build y BPS independiente,11pruebas de infraestructura y checksum están aprobados; no confundirlos con aprobación final del juego.
