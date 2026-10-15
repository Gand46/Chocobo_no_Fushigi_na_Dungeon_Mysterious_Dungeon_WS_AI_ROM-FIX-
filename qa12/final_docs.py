from pathlib import Path
import json,hashlib,shutil,csv
w=Path.cwd();root=w/'delivery/Chocobo_EN_v1.1_HF9_TEST_Fuentes_QA12_20261014';delivery=root.parent
m=json.loads((root/'manifest.json').read_text());v=json.loads((w/'qa12/validation.json').read_text());bps=w/'private_roms/hf9_release/Chocobo_EN_v1.1_HF9_TEST_JP_CCAA4853.bps'
assert hashlib.sha256(bps.read_bytes()).hexdigest()==m['bps_sha256']
for p in [root/'patches'/bps.name,delivery/bps.name]:shutil.copy2(bps,p)
shutil.copy2(w/'private_roms/hf9_release/build_result.json',root/'docs/QA12_BUILD_RESULT.json')
p=root/'tools/verify_evidence.py';s=p.read_text().replace("startswith((", "startswith(('PROPERTY_', 'ITEM_', ").replace('patches/Chocobo_EN_v1.1_HF8_TEST','patches/Chocobo_EN_v1.1_HF9_TEST');p.write_text(s)
issues=json.loads((root/'docs/issue_register.json').read_text())
for i in issues:
 if i['id']=='TR-01':i.update(status='PARTIAL_255_ITEM_IDS_PLUS_96_PROPERTY_DESCRIPTORS',scope='QA10:92 equipment IDs. QA12:163 remaining IDs01..64/C1..FF on HF8, including125 nonblank and38 blank names, not all obtainable items. HF9 final:96 nonzero property descriptions in49 pairs plus9 targeted cases. Four visible text defects fixed. Global dialogue/layout/linguistic approval remains open.')
 if i['id']=='EN-01':i.update(status='NOT_REPRODUCED_VALID_FUSED_PROPERTY_FIXTURES',scope='Native synthesis metadata located: flag10, linked10-byte record at6D3F, property codes in bytes8/9; aux is not the property field. HF9:49 pairs cover all57 talon and39 saddle nonzero descriptions;9 targeted checks include both positions,cursed gear and -99. No four watched-store overruns or175AC..17F8F writes. Invalid item IDs used as property IDs caused diagnostic overruns and are explicitly excluded. Exact historical freeze/save-loss trigger, natural fusion acquisition and all combinations remain open.')
(root/'docs/issue_register.json').write_text(json.dumps(issues,indent=2)+'\n')
with (root/'docs/issue_register.csv').open('w',newline='') as f:
 c=csv.DictWriter(f,fieldnames=['id','status','scope']);c.writeheader();c.writerows(issues)
q=json.loads((root/'docs/quality_gates.json').read_text());q.update(version='HF9_TEST',build='PASS_FINAL_PINNED_SHA256',independent_bps='PASS_EXACT_FINAL_SHA256',text_global_layout='PARTIAL_255_BYTE_IDS_ACROSS_QA10_QA12_PLUS_96_PROPERTIES;GLOBAL_NOT_APPROVED',equipment_cause='NOT_REPRODUCED_VALID_FUSED_RECORDS',qa12_four_repairs='PASS_NATIVE_JP_CONTROLS_AND_FINAL_HF9',qa12_property_surface='PASS_96_DESCRIPTORS_49_PAIRS_FINAL_HASH',qa12_targeted_native_checks='PASS_9_CASES_FINAL_HASH',qa12_differential_images='147_COMPARED;144_IDENTICAL;3_DIFFER_ONLY_IN_REPAIRED_ROW',qa12_byte_scope='19_CHANGED_BYTES_VS_HF8;FOUR_TEXT_SLOTS_AND_CHECKSUM_ONLY',text_census='2333_ENTRIES_19_FAMILIES_NO_CROSS_SLOT_CANDIDATES;NOT_LAYOUT_APPROVAL',final_approved=False)
(root/'docs/quality_gates.json').write_text(json.dumps(q,indent=2)+'\n')
(root/'docs/approval_matrix.json').write_text(json.dumps({'scope':'HF9 four native-text repairs; no global or historical-bug approval','DISCOVERED':'PASS_NATIVE_BASELINE_AND_JP_CONTROLS','TRANSLATED':'PASS_FOUR_REPAIRS_ONLY','INTEGRATED':'PASS_BOUNDED_SLOTS_NO_POINTER_FONT_OR_CODE_CHANGE','RUNTIME_CONFIRMED':'PASS_FINAL_HASH_SYNTHETIC_SETUP_NATIVE_INPUTS','LINGUISTIC_APPROVED':'PASS_FOUR_SCOPED_MEANINGS;GLOBAL_OPEN','TYPOGRAPHY_APPROVED':'EXISTING_FONT_UNCHANGED;NO_NEW_GLYPHS','LEGIBILITY_APPROVED':'DIRECT_NATIVE_SCREEN_REVIEW_ONLY','DESIGN_APPROVED':'EXISTING_LAYOUT_AND_USER_LOGO_UNCHANGED','VISUAL_APPROVED':'PASS_SCOPED_FOUR_REPAIRED_TEXTS;GLOBAL_OPEN','FUNCTIONAL_APPROVED':'PASS_SCOPED_MENU_RETURN_AND_INVENTORY;NO_HISTORICAL_FREEZE_REPRODUCTION','FINAL_APPROVED':False,'inherited_title_gate':'HF8 independent context-masked logo glyph review remains pending; pixel integration and runtime evidence retained unchanged'},indent=2)+'\n')
readme='''# Chocobo English v1.1 + HF9 TEST

Corrige cuatro textos visibles: propiedad contra no muertos, ataque de tres direcciones, elemento de fuego en silla y nombre de Sleep Card. Conserva el logo aportado y todos los fixes HF1–HF8. TEST: la causa del bloqueo histórico por equipamiento no está resuelta.

Aplicar `patches/Chocobo_EN_v1.1_HF9_TEST_JP_CCAA4853.bps` directamente a la ROM japonesa original CRC32 `CCAA4853`. Sin parches intermedios. No se distribuyen ROM, BIOS ni emulador.

## Reconstruir

`python3 build.py JP.ws --out build`

Python 3, sin dependencias externas para el build. `BUILD.bat` y `BUILD.command` conservados; no probados en Windows/macOS durante QA12. Verifica base, preimágenes, rangos, checksum y hash final.

`python3 tools/verify_independent_bps.py JP.ws`

## Fuentes y pruebas

Ediciones acumulativas: `src/corrections.json`. Textos nuevos y procedencia japonesa: `localization/hf9_text_repairs.json`. Se reutiliza la fuente nativa, sin dibujar glifos ni mover punteros. Los bytes sobrantes después del nuevo terminador de tres direcciones son inalcanzables; el slot siguiente queda intacto.

Pruebas portables y comandos: `docs/QA12_METODO_Y_LIMITES.md`. Evidencia de esta fase: `evidence/qa12_runs/`. Las pruebas históricas mantienen sus hashes y no se presentan como nuevas ejecuciones de HF9. `docs/issue_register.json` es la lista vigente de pendientes.

Logo vigente: `assets/title/user_v01`; importador `tools/integrate_title_assets.py`; integración documentada en `docs/QA11_INTEGRACION_LOGO.md`. No volver al rótulo provisional HF7.

Consultar `INFORME_ES.md`, `manifest.json`, `docs/quality_gates.json` y `CONTEXTO_CONTINUACION.md`.
'''
(root/'README.md').write_text(readme)
report=f'''CHOCOBO — HF9 TEST / QA12 — 14 de octubre de 2026

Se corrigieron cuatro defectos visibles heredados de la traducción inglesa:
1. La propiedad contra no muertos mostraba «Skill Strong on dead o,af». Ahora usa «Skill Strong to Undead!», con los glifos ya empleados por ZombieKiller.
2. El ataque de tres direcciones mostraba «Skill3pronged hit o,af». Se termina la cadena después de «hit».
3. La propiedad de fuego de las sillas mostraba «Fire typeaf». Ahora coincide con «Fire type» de las garras.
4. La carta de sueño mostraba «Sleepel Card». Se quitó el glifo sobrante: «Sleep Card».

Los significados se contrastaron en la ROM japonesa mediante siete casos de control. Se conservan el logo entregado, animación, fuente, punteros, código de juego y fixes anteriores. HF9 modifica 19 bytes respecto de HF8: 17 bytes de texto y dos de checksum.

Validación y cobertura
Se exploraron 163 identificadores adicionales (01–64 y C1–FF) mediante inventario sintético y menú nativo: todos conservaron el objeto y regresaron del menú. Incluyen 125 nombres no vacíos y 38 vacíos; no se afirma que todos sean objetos obtenibles. Sumados a los 92 IDs revisados en QA10, cubren los IDs 01–FF en esas superficies, no todos los textos del juego.

Se identificó el registro nativo de propiedades fusionadas. La bandera 10 activa un registro de diez bytes vinculado al espacio de la bolsa; sus bytes 8/9 contienen códigos de propiedad. No se guardan en el campo auxiliar del objeto. Las familias 6 y 7 contienen 57 y 39 descripciones no nulas.

En el hash final HF9 se ejecutaron 49 parejas que cubren las 96 descripciones, más nueve casos dirigidos que incluyen los textos corregidos en ambas posiciones, la carta y dos equipos malditos con nivel -99. Todos terminaron sin apagar la CPU, conservaron el registro de inventario y regresaron al menú. No hubo cruces del límite en los cuatro puntos de copia vigilados ni escrituras en 175AC–17F8F. Son pruebas sintéticas con controles nativos; no son fusiones adquiridas jugando ni todas las combinaciones posibles.

Comparación de 147 capturas nativas HF8/HF9 de propiedades: 144 idénticas; las otras tres cambian únicamente en la línea corregida. Se revisaron las pantallas completas a resolución nativa. Censo de 2.333 recursos en 19 familias: sin candidatos que pierdan el terminador antes del siguiente slot; esto no aprueba su traducción ni maquetación global.

Build fijado a hash, aplicación BPS independiente y 11 pruebas existentes de infraestructura: PASS. Fuentes acumulativas y BPS directo desde la JP incluidos. Segundo emulador y hardware: sin validar.

Qué sigue abierto
• Maquetación y revisión lingüística global, especialmente diálogos, ventanas y variantes fuera de los menús examinados.
• Disparador histórico del bloqueo al consultar equipamiento. No se reprodujo con registros de propiedad válidos. Seis casos con los antiguos terminadores defectuosos de la traducción también regresaron; por eso no se presentan como causa confirmada del congelamiento.
• Obtención y combinación natural de equipo, inventarios completos y el estado exacto que falla en los reportes.
• Variante histórica de Atla: el rescate exacto D2F60 ya tiene PASS sintético acotado QA10; su congelamiento original continúa sin reproducirse.
• Ascensor continuo, ruta natural 99→30 y causa natural del reset del guardado. Se conservan los fixes y pases acotados anteriores.
• Revisión formal independiente de legibilidad del logo aportado. Su integración y fidelidad de píxeles siguen verificadas en QA11.

Se excluyen expresamente de la cobertura válida dos pruebas diagnósticas: un selector de menú inicialmente incorrecto y una primera construcción de propiedades que usaba IDs de objetos fuera del rango permitido. Esta última produjo desbordamientos artificiales y no demuestra un fallo alcanzable jugando. Los registros se conservan etiquetados para no confundirlos con un PASS ni con la causa del fallo histórico.

Identidad
JP SHA-256: {m['original']['sha256']}
HF9 SHA-256: {m['target']['sha256']}
HF9 CRC32: {m['target']['crc32']}; checksum WS: {m['target']['ws_checksum']}.
BPS SHA-256: {m['bps_sha256']}
Estado inicial de pruebas SHA-256: 2cb9e29b3749ce0caf9628ff93f8c5b52ebe5eb7212627175290a38d9adb5f82.
Entorno: Linux x86_64, Mesen 2.1.1. TEST, sin aprobación global ni causa histórica cerrada. Incidente físico eléctrico fuera del alcance ROM.
'''
(root/'INFORME_ES.md').write_text(report);(delivery/'Informe_Chocobo_HF9_QA12_20261014.txt').write_text(report)
(root/'CHANGELOG.md').write_text('''# Changelog

## HF9 TEST — QA12 — 2026-10-14

- Cuatro correcciones de texto nativo; 19 bytes modificados respecto de HF8, incluidos los dos de checksum.
- Nuevo mapa del registro de síntesis y pruebas de las 96 descripciones de propiedades en 49 parejas.
- Amplía revisión a 163 IDs fuera del rango de equipamiento de QA10; conserva blancos/reservados como tales.
- Evidencia final de ambos órdenes de propiedades y equipo maldito; no declara reproducido el bloqueo histórico.
- Fuentes completas, BPS directo y limitaciones explícitas. Historial anterior en `docs/history/hf8_qa11/CHANGELOG.md`.
''')
context='''# Continuación tras HF9 / QA12

Autoridad: manifest.json y build.py de HF9. ROM final SHA256 c91c1f57485dac8237724a148e19181a42dfd82cfb6fd3d2661ff9b93ad49284; CRC4CA9F7B4; checksumE8BA. BPS acumulativo sobre JP CCAA4853. Cuatro fixes en localization/hf9_text_repairs.json. Sólo19bytes nuevos vsHF8, incluidos checksum; logo y lógica intactos.

QA12 verificó163IDs adicionales al rango65..C0 deQA10, con125nombres no vacíos y38vacíos. No confundir255IDs inspeccionados con255objetos obtenibles ni conmaquetación global. El selector Check es familia1 índice4, NO6; primera corrida item_layout está excluida y se corrigió en item_check_fixed.

Descubrimiento útil: bandera10 de inventario activa tabla de síntesis SRAM6D3F,117registros de10bytes. Byte0=espacio de bolsa; bytes8/9=códigos de propiedades. Talon familia6 rango0..57; Saddle familia7 rango0..39. Aux de inventario NOespropiedad. Lectores19B16A y19B243; compositor184AAF..184B07. qa12/property_all copia estadísticas base y usa códigos válidos. La primera fused_records usabaIDsdeobjetos, es inválida y sus206cruces no prueban el bug original.

FinalHF9:49parejas cubren96descripciones y9casos críticos. Sincruces en cuatro stores vigilados, sinwrites175AC..17F8F, retornoe inventario conservados. Comparación147capturas:144idénticas y3sólo cambianlalíneacorregida. No se adquirieron fusiones jugando ni se probarontodaslasparejas. Siguientespruebas útiles:producción natural deunregistro fusionado, bolsa completa/dos selecciones, estado exactodelreporte; no repetir barridosbásicossinriesgo nuevo.

Pendientes: maquetaciónglobal; causahistórica delbloqueo deequipo; variantehistóricadeAtla (rescateexactoD2F60 yaPASSsintéticoQA10); ascensorcontinuo/rutanatural99→30; causanaturaldelreset. Logo vigente assets/title/user_v01, integraciónQA11conservada;revisiónformalindependientedeglifospendiente. No rediseñarelartedelusuario. Incidenteeléctricofísicofueradealcance. No repetirguardado,Lafoss,eventosotítulocerradossinsucambioconcreto.

Comandos y límites en docs/QA12_METODO_Y_LIMITES.md. Evidencias originales conservan sus hashes. QA12 no concede aprobación final/global. Ahorro de tokens no medido.
'''
# Keep continuation prose readable for the next phase.
context=context.replace('Sincruces','Sin cruces').replace('sinwrites','sin writes').replace('retornoe','retorno e').replace('No se adquirieron fusiones jugando ni se probarontodaslasparejas. Siguientespruebas útiles:producción natural deunregistro fusionado, bolsa completa/dos selecciones, estado exactodelreporte; no repetir barridosbásicossinriesgo nuevo.','No se adquirieron fusiones jugando ni se probaron todas las parejas. Siguientes pruebas útiles: producción natural de un registro fusionado, bolsa completa/dos selecciones, estado exacto del reporte; no repetir barridos básicos sin riesgo nuevo.')
(root/'CONTEXTO_CONTINUACION.md').write_text(context)
(root/'docs/QA12_METODO_Y_LIMITES.md').write_text('''# QA12 — método, procedencia y límites

## Reproducir el menú de propiedades

Tras reconstruir HF9, proporcionar un Mesen2.1.1 privado:

`python3 qa12/property_all/run_suite.py build/Chocobo_EN_v1.1_HF9_TEST.ws evidence/qa12_fixtures/checkpoint.mss runs/property_final --suite equipment --mesen /ruta/Mesen --timeout 150`

Para las nueve regresiones concretas, reemplazar `property_all` por `critical_check`. Una instancia por perfil/directorio Mesen; no compartir Saves entre procesos.

El estado inicial procede de q3_dungeon, identificado por SHA256 en QA12_RUN_INDEX.json. Es sintético. El observador carga el estado en un callback único de CPU, escribe un registro de bolsa en6C9F y, cuando corresponde, un registro de síntesis en6D3F. Conserva estadísticas del objeto base y añade códigos de propiedad válidos. El resto del recorrido usa botones del menú nativo. No inyecta punteros ni sustituye retornos del getter.

Registro de bolsa: cantidad,ID,nivel,aux,flags. Para talones:19B663,54entradas de15bytes; propiedad base enbyte14. Para sillas:19B98D,36entradas de14bytes; propiedad base enbyte13. Bandera10selecciona tablaSRAM6D3F de117registros de10bytes. Byte0vincula espacio de bolsa, noIDdeobjeto; bytes8/9son propiedades. Familia6tabla15C918(58entradas), familia7tabla15CF54(40). El código0indica ausencia; se cubren las96entradas no nulas en49parejas, no el producto cartesiano de combinaciones.

Vigilancia: stores CPU37AFF,37B7D,37BC1,37BFD conDI>=023C, donde el buffer6057alcanzaría el puntero6293; escriturasCPU175AC..17F8F. Ausencia de hits significa sólo ausencia en esos puntos/rango durante estos recorridos. No es un análisis de todas las escrituras ni prueba general de persistencia. Se comprueban gettersfamilias6/7, salida sinpowerOff, estado menú0004 e inventario conservado.

`python3 qa12/verify_scope.py --hf8 /ruta/HF8.ws --hf9 build/Chocobo_EN_v1.1_HF9_TEST.ws --runs evidence/qa12_runs --out /ruta/validation.json`

Pillow se requiere sólo para comparar las capturas. Verifica19bytes dentro de los cuatro slots ychecksum, hashes finales, coberturas, retornos y147capturas; noaprueba gameplay natural. El build normal no requierePillow.

## Corridas que no conceden cobertura

q12_item_layout: buscabaacción6(Equip), no4(Check); consumió algunos objetos. Excluida. q12_item_check_fixed es la repetición corregida y sus163casos conservan inventario y muestran el getter de descripción esperado.

q12_fused_records: usó IDsdeobjetos como códigosdepropiedad, fuera de los límites de familia. Produjo206hits de buffer con datos inválidos; NOes reproducción del congelamiento reportado. q12_fusion_probe sólo probóflags/aux sin registro vinculado y NOcubre propiedades fusionadas. Se retienen estas evidencias por trazabilidad.

q12_property_all_hf9: candidato intermedio antes del arregloSleepCard; noes hashfinal. La prueba válida final es q12_property_final_hf9. Los metadatos originales no se reescriben.

q12_legacy_fused: seis parejas de propiedades11/12/13enEnglishv1.1. Se ve la concatenación por terminadores históricos, pero todos los casos regresan: NOprueba que ese defecto fuera la causa histórica del bloqueo. HF1ya había corregido sus terminadores.

## Controles y alcance

Siete casos JP verifican significados y textos originales. HF9loscorrige sinmodificar fuente,punteros,código ni recursos del logo. Los casos finales no prueban adquisición natural de fusiones, efectos de combate, todas las combinaciones o datos de guardado reales del reporte. Los antiguos casos de guardado,Lafoss,Atla ylogo permanecen heredados poridentidad debytes y sus limitaciones; no se declaran reejecutados.

Se revisó nuevamente el reporte público de jugadores en https://retroachievements.org/game/16362 :describe congelamiento al consultar equipo y pérdida de guardado, sinidentificarobjeto, combinación o estado reproducible en el contenido consultado. Es una pista, no una causalidad demostrada. Las pruebas sintéticas no cierran EN-01 ni SAVE-01natural.
''')
(root/'docs/QA12_VALIDATION_SUMMARY.json').write_text(json.dumps({'build':'PASS_PINNED_FINAL','independent_bps':'PASS','existing_unit_tests_passed':11,'text_resources_new':4,'runtime_final_sha256':m['target']['sha256'],'scope_verification':v,'item_baseline':json.loads((w/'qa12/item_coverage.json').read_text()),'final_approved':False},indent=2)+'\n')
print('Current HF9 documents and BPS prepared')
