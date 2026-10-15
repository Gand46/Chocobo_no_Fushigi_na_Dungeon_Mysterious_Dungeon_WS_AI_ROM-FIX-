from pathlib import Path
import json,csv,hashlib
root=Path('delivery/Chocobo_EN_v1.1_HF6_TEST_Fuentes_QA9_20261014');m=json.loads((root/'manifest.json').read_text())
report='''CHОCOBO — HF6 TEST / QA9 — 14 de octubre de 2026

Se incorpora una corrección de la caché decimal del piso. Reproduce y corrige dos resultados concretos: el bucle de carga de F99 con caché desactualizada y la asignación de un mapa de jefe a F30 al reconstruir la entrada con el estado dejado por Telep desde F99. La versión sigue siendo TEST; no es una aprobación global.

RESULTADOS Y PENDIENTES

• Pisos/ascensor: corregida la consulta de dígitos obsoletos en los selectores de D3. Doce destinos sintéticos —11,22,33,44,55,66,77,88,98,99,100 y30— alcanzan una escena de piso. No todos son pisos de jefe: el código nativo omite el evento de77. La entrada continua por el ascensor todavía no queda aprobada.
• Telep99→30: se ejecutó Use con Telep Card0B en F99 y se regresó al pueblo. Con ese bloque vivo se preparó una reentrada sintética a30 y se utilizó el cargador nativo. HF5 asigna el estado de mapa A217; HF6 asigna0000 y muestra un piso ordinario. Es PASS sintético de la reconstrucción y de la asignación del mapa. No equivale a recorrer el ascensor de forma continua ni demuestra el congelamiento posterior al caminar citado en el foro.
• Fuente/rana: mapeados los contadores7514/7515 y flags54..59. Se probaron dos configuraciones coherentes antes del final:15Geyser+5Frog y45Geyser+15Frog, con sus flags acumulados. Ambas completan E0:ABE2 en HF5; la variante completa también lo hace en HF6. Se conserva evidencia de control posterior. No se ha reproducido el bloqueo del foro ni aplicado un parche especulativo a esta escena.
• Maquetación global: se revisó visualmente el selector de piso y se conserva el censo previo de2.333 entradas/19familias. No se detectó un nuevo defecto de maquetación en esa pantalla. Continúa pendiente revisar globalmente diálogos, tiendas, eventos y créditos en sus consumidores reales.
• Título: permanece japonés. Los411tiles nativos y su cargador siguen identificados; falta diseñar e integrar el arte inglés respetando el estilo del logotipo. Esta versión no sustituye el título por una fuente genérica.
• Equipamiento: no se ha reproducido la causa del bloqueo; siguen vigentes los ensayos acotados anteriores. No se añade un fix de equipamiento sin un disparador demostrado.
• Atla: el rescate exacto del testimonio continúa sin validar. La fuente Yahoo no pudo consultarse de nuevo. Las escenas ya completadas no se renombran como prueba de ese incidente.

CAUSA Y CAMBIO CONCRETO

El piso autoritativo reside en7303 y sus cinco dígitos decimales en753A..753E. El selector de eventos consulta estos últimos. Si pertenecen a otro piso, puede omitir un mapa especial o seleccionar uno ajeno. En la carga sintética de F99 con caché61, omite el evento y llega a148393: solicita una colocación aleatoria hasta que4B54 sea distinto de cero. La probabilidad0647 vale cero;1EEAFB rechaza cada intento. La copia del guardado, en cambio, ya había concluido íntegramente.

HF6 recalcula los dígitos mediante la rutina original9000:6E1C solo cuando el opcode34 lee753A..753E dentro de los selectores E1:639C..69FF. El gancho está en14D398 y el código nuevo en14FDA8..14FDD9. Preserva registros y flags, vuelve al consumidor nativo y deja intactos los valores temporales del menú del ascensor. No fuerza la probabilidad del mapa, no inventa un evento y no salta las escenas.

Hay53bytes distintos frente a HF5:51de contenido y2de checksum. Se conservan acumulativamente los arreglos de texto, Whistle, Lafoss y protección del guardado de HF1–HF5.

VALIDACIÓN BASADA EN DATOS Y LÍMITES

Las pruebas distinguen adquisición/preparación sintética de ejecución nativa. Las fixtures antiguas modificaban el número de piso conservando la caché61 de otro contexto. Esto explica sus pantallas blancas; por sí solo no demuestra que una partida natural produzca esa incoherencia. Un control nuevo coloca una escalera junto al personaje de F98 y el juego ejecuta Save and go on. El guardado nativo contiene piso98/caché98 y carga correctamente F99 tanto con HF5 como con HF6. Por tanto, no se presenta ese caso como una corrupción del guardado original.

En la prueba de Telep, la salida99→pueblo es nativa, con una carta inyectada en la bolsa. La reentrada utiliza el bloque realmente dejado en el pueblo, conservando su caché99; se cambia D3 y piso29 en el contenedor guardado para que el cargador entre a30. Cambian el contenedor y esos campos, no se falsifica una pulsación del ascensor. La diferencia A217→0000 demuestra el efecto de la corrección en ese estado; la ruta continua sigue pendiente.

Los intentos de invocar directamente los guiones del ascensor se conservaron como diagnósticos incompletos y se excluyeron del PASS. También se excluye como corrección la sonda que cambiaba0647a1: liberaba el bucle, pero no garantizaba recuperar el mapa previsto. Las primeras hipótesis de flags4D/12 no correspondían a fuente/rana.

Build directo desde JP, checksum, aplicador BPS independiente, consistencia histórica de recursos y11pruebas de infraestructura: PASS. QA9_VERIFICATION.json comprueba los offsets permitidos, los destinos, los estados de mapa y las copias nativas exactas de2.516bytes. Segundo emulador, hardware y recorrido natural completo no están aprobados. El bloqueo eléctrico del cartucho permanece cerrado y fuera del alcance de esta corrección.

APLICACIÓN

Aplicar Chocobo_EN_v1.1_HF6_TEST_JP_CCAA4853.bps directamente a la ROM japonesa limpia CRC32CCAA4853, sin encadenar HF5. Los fuentes reconstruidos son editables y acumulativos; no son el código fuente original del juego. No se incluyen ROM ni BIOS.

HF6 conserva el formato de guardado protegido HF4/HF5. Para volver a una revisión anterior aHF4, exportar una copia con tools/chocobo_save.py --export-legacy; no sobrescribir el guardado de trabajo. La protección rechaza bloques incompletos y no recupera automáticamente una generación sobrescrita.

FUENTES EXTERNAS DEL CASO

Los siguientes enlaces son testimonios, no pruebas de causalidad del código:
https://wazap.com/cheat/セーブデータ破損？バグ/570082/ — pisos y comentario2729953 de Telep99→30.
https://wazap.com/cheat/クリア不能バグと対処法/570080/ — fuente/rana antes del segundo final.
https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14305291199 — referencia retrospectiva de Atla; inaccesible en esta revisión.
Chat compartido revisado en QA6: https://chatgpt.com/share/6acebdec-2b5c-83e9-833e-60560c52d788
'''
hashes=f"\nIDENTIFICACIÓN\nJP SHA256: {m['original']['sha256']}\nHF6 SHA256: {m['target']['sha256']}\nHF6 CRC32: {m['target']['crc32']}; checksum WS: {m['target']['ws_checksum']}\nBPS SHA256: {m['bps_sha256']}\n"
(root/'INFORME_ES.md').write_text(report+hashes);Path('delivery/Informe_Chocobo_HF6_QA9_20261014.txt').write_text(report+hashes)
(root/'README.md').write_text('''# Chocobo English v1.1 + HF6 TEST

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

Usar SRAM cruda de32KiB; no confundirla con savestates. La protección no recupera un bloque anterior sobrescrito.
'''+hashes)
(root/'CHANGELOG.md').write_text('''# HF6 TEST / QA9 — 2026-10-14

- Recalcula los dígitos del piso únicamente al leerlos en los selectores D3 E1:639C..69FF.
- Corrige la carga sintética de F99 con caché desactualizada y el mapa incorrecto de F30 en la reentrada basada en el estado posterior a Telep99.
- Comprueba12destinos, carga de guardado nativo coherente y dos variantes fuente/rana.
- Mantiene separados los ensayos sintéticos aprobados, los diagnósticos y las rutas incompletas.
- Conserva HF1–HF5;53bytes cambiados frente aHF5, incluidos2de checksum.

Historial anterior: docs/history/hf5_qa8.
''')
updates={
'TR-01':('PARTIAL_NATIVE_FLOOR_MENU_REVIEW_GLOBAL_PENDING','Native floor chooser visually reviewed; prior terminator fixes/census retained. No global layout PASS.'),
'JP-01':('FIXED_SCOPED_SYNTHETIC_STALE_FLOOR_CACHE','HF6 refreshes floor digits only in D3 event selectors;12cold-load destinations. Native coherent save98->load99 passes both HF5/HF6. Continuous elevator route and natural save-loss trigger remain unvalidated.'),
'JP-02':('COHERENT_FOUNTAIN_FROG_VARIANTS_NO_FAILURE_REPRODUCED','Minimum15Geyser+5Frog and full45+15 synthetic states complete ending; HF6 full variant repeats completion. No fountain-specific binary fix.'),
'JP-03':('FIXED_SCOPED_SYNTHETIC_REENTRY_MAP','Native Telep99->town followed by synthetic saved-data reentry30: HF5 mapA217, HF6 ordinary0000. Continuous elevator route and subsequent reported freeze not reproduced.'),
'JP-04':('NOT_VALIDATED_RESCUE','Exact retrospective Atla incident remains unvalidated; source Yahoo inaccessible. Do not relabel D1 or generic ending as the exact rescue reproducer.')}
issues=json.loads((root/'docs/issue_register.json').read_text())
for row in issues:
 if row['id'] in updates:row['status'],row['scope']=updates[row['id']]
(root/'docs/issue_register.json').write_text(json.dumps(issues,indent=2)+'\n')
with (root/'docs/issue_register.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=['id','status','scope']);w.writeheader();w.writerows(issues)
g=json.loads((root/'docs/quality_gates.json').read_text());g.update(version='HF6_TEST',floor_cache='PASS_SCOPED_SYNTHETIC_D3_12_DESTINATIONS',fountain_frog_before_ending='PASS_SYNTHETIC_COHERENT_VARIANTS_NO_REPRODUCED_FAILURE',teleport99_to30='PASS_SYNTHETIC_REENTRY_MAP_ONLY_CONTINUOUS_ELEVATOR_PENDING',actual_elevator_ui='NOT_VALIDATED',save_protected_normal_load='PASS_HF5_NATIVE_SAVE98_COLD_LOAD_BOTH_HF5_HF6',assembly_rebuild='PASS_SCOPED_FLOOR_GUARD_BYTE_IDENTICAL',final_approved=False);(root/'docs/quality_gates.json').write_text(json.dumps(g,indent=2)+'\n')
(root/'docs/approval_matrix.json').write_text(json.dumps({'scope':'HF6 scoped floor-cache correction','discovered':'PASS_NATIVE_CODE_AND_RUNTIME','integrated':'PASS_PREIMAGE_ALLOWED_DIFF','runtime':'PASS_SYNTHETIC_COLD_LOAD_AND_MAP_ASSIGNMENT','linguistic_typography':'NO_TEXT_OR_FONT_EDITS_GLOBAL_PENDING','visual':'PASS_SCOPED_FLOOR_RECONSTRUCTION','functional':'PASS_SCOPED_SYNTHETIC','final_approved':False,'pending':'global layout, English title, equipment cause, natural elevator route, original fountain failure and exact Atla rescue'},indent=2)+'\n')
(root/'CONTEXTO_CONTINUACION.md').write_text('''# Continuación después de HF6 / QA9

Build vigente HF6 TEST; ver manifest.json y docs/QA9_REPRODUCTION.md. No repetir auditorías históricas completas. Fallo físico eléctrico cerrado.

Nuevo fix: opcode34 en14D398 salta a14FDA8..14FDD9; solo bancoE1, puntero639C..69FF y dirección753A..753E. Recalcula dígitos mediante9000:6E1C desde piso7303, conserva registros/flags y vuelveD39B. Bucle blanco148393 espera4B54;0647=0 impide siempre aceptación1EEAFB. No usar parche de probabilidad1: omitía mapa especial.

Control crucial: fixtures post-ending modificabanfloor y dejaban cache61. HF5 concache98 coherente carga99; guardado nativo Save and go on desde98 también es coherente y pasa HF5/HF6. La causa natural de reset/ascensor sigue abierta.

Telep: carta0B, nativeUse desdeF99->pueblo conserva cache99. Fixture post_telep99_reentry30 copia ese bloque vivo acontendorlegacy y cambiaD3/current=max29. HF5 generaA217en30;HF6genera0000. Esto es reproducción sintética de datos, no secuencia continua del ascensor. CheckpointHF6 de30 disponible. Intentos de scriptentry incompletos están excluidos. E0:2873 es menú Go to which floor; temporal060E, flags7558/59; native25/20 decrece7303en18C83F. Entry del script requiere1FAE5 además649F80,pero falta reproducir su llamador completo/retorno para continuar sin pantalla de transición. No confundirE0:2D7Econelascensorfinal.

Fuente/rana:194E8C..4F7E incrementa7514porID09(Geyser) y7515porID04(Frog);15/30/45Geyser activa54/55/56 y suma20/40/60activa57/58/59. En7313masks0010..0200. Variantes coherentes mínima0090(15+5),completa03F0(45+15),antesdeljefeD2,terminanE0:ABE2. Flags4D/12eranhipótesisdescartada. Esperarreproductornaturalantesdeinventarfix.

Pendientes: títuloinglésconartefiel, maquetaciónglobal, disparadorequipamiento, ascensorcontinuoy99->30sincontenedorintermedio, fallooriginalfuente/rana, rescateAtlaexacto. FuenteYahooinaccesible; nodarporcerrado conD1F30.

Próximo trabajo: trazar la entrada auténtica al menú2873 desde el pueblo (llamador/mode1FA6/1FAE), capturar dígitos antes/después de18C83F, comparar seleccion30/99. Mantener preimágenes y no modificar recursos del título con tipografía genérica.
''')
print('Docs written')
