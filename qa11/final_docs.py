from pathlib import Path
import json,hashlib,shutil,csv,datetime
w=Path.cwd();root=w/'delivery/Chocobo_EN_v1.1_HF8_TEST_Fuentes_QA11_20261014';delivery=root.parent
m=json.loads((root/'manifest.json').read_text());bps=w/'private_roms/hf8_release/Chocobo_EN_v1.1_HF8_TEST_JP_CCAA4853.bps';m['bps_sha256']=hashlib.sha256(bps.read_bytes()).hexdigest();(root/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
for dst in [root/'patches'/bps.name,delivery/bps.name]:shutil.copy2(bps,dst)
shutil.copy2(w/'private_roms/hf8_release/build_result.json',root/'docs/QA11_BUILD_RESULT.json')
shutil.copy2(root/'CONTEXTO_CONTINUACION.md',root/'docs/history/hf7_qa10/CONTEXTO_CONTINUACION.md')
q=json.loads((root/'docs/quality_gates.json').read_text());q.update(version='HF8_TEST',title_translation='PASS_USER_SUPPLIED_ENGLISH_LOGO_RUNTIME',title_glyph_review='NOT_VALIDATED_INDEPENDENT_REVIEW_OF_NEW_USER_ART; HF7_36_GLYPH_PASS_SUPERSEDED',title_pixel_fidelity='PASS_1001_FRAMES_ROWS64_120_EXACT_SOURCE_INDICES_WITH_NATIVE_PALETTE',title_animation='PASS_TOP56_AND_FOOTER_IDENTICAL_TO_HF7_IN_1001_FRAMES;64_ANIMATION_TILES_AND_CODE_BYTE_IDENTICAL',title_boot_menu_gameplay='PASS_SCRIPTED_NATURAL_BOOT_MENU_NEW_GAME_VILLAGE;SAVESTATE_NATIVE_WALK',final_approved=False);(root/'docs/quality_gates.json').write_text(json.dumps(q,indent=2)+'\n')
(root/'docs/approval_matrix.json').write_text(json.dumps({'scope':'HF8 user supplied English title v0.1 integration only','DISCOVERED':'PASS','TRANSLATED':'PASS_SUPPLIED_ENGLISH_TITLE','INTEGRATED':'PASS_NATIVE_2BPP_MAPS_AND_PALETTE','RUNTIME_CONFIRMED':'PASS_SCRIPTED_NATURAL','LINGUISTIC_APPROVED':'PASS_TITLE_TEXT_ONLY','TYPOGRAPHY_APPROVED':'NOT_VALIDATED_INDEPENDENT_REVIEW_OF_SUPPLIED_STYLIZED_ART','LEGIBILITY_APPROVED':'NOT_VALIDATED_INDEPENDENT_CONTEXT_MASKED_REVIEW','DESIGN_APPROVED':'PASS_SCOPED_FAITHFUL_INTEGRATION_OF_USER_SELECTED_ART','VISUAL_APPROVED':'NOT_VALIDATED_FORMAL_INDEPENDENT_GLYPH_GATE;RUNTIME_PIXEL_FIDELITY_PASS','FUNCTIONAL_APPROVED':'PASS_SCOPED_TITLE_ANIMATION_MENU_NEW_GAME_VILLAGE_WALK','FINAL_APPROVED':False,'note':'Direct native visual review reads Chocobo\'s / Mystery Dungeon / for WonderSwan. It was not blind to expected content; no formal independent legibility PASS is claimed. No glyphs of the supplied design were redrawn. Shared game font is unchanged.'},indent=2)+'\n')
issues=json.loads((root/'docs/issue_register.json').read_text())
for i in issues:
 if i['id']=='TR-03':i.update(status='USER_LOGO_V01_INTEGRATED_RUNTIME_CONFIRMED',scope='HF8 replaces the HF7 title with the supplied pixel art. 139 native patterns, map lengths247/625, 1001-frame static-pixel and upper/footer comparison, copyright, prompt, menu and natural new game checked. Formal context-independent glyph review remains open; prior HF7 glyph approval does not transfer.')
(root/'docs/issue_register.json').write_text(json.dumps(issues,indent=2)+'\n')
with (root/'docs/issue_register.csv').open('w',newline='') as f:c=csv.DictWriter(f,fieldnames=['id','status','scope']);c.writeheader();c.writerows(issues)
readme='''# Chocobo English v1.1 + HF8 TEST

Integra el logo inglés aportado por el usuario y conserva todas las correcciones de HF1–HF7. Versión TEST, no RC ni aprobación global.

Aplicar `patches/Chocobo_EN_v1.1_HF8_TEST_JP_CCAA4853.bps` directamente a la ROM japonesa original CRC32 `CCAA4853`. No requiere parches intermedios. La ROM, BIOS y emulador no se distribuyen.

## Reconstruir

`python3 build.py JP.ws --out build`

Python 3 sin dependencias externas para el build normal. En Windows: `BUILD.bat "C:\\ruta\\JP.ws"`; lanzador conservado, no probado en Windows durante QA11. El build verifica la base, preimágenes, rangos, checksum y hash de la versión publicada.

## Editar el nuevo logo

Fuentes canónicas: `assets/title/user_v01/assets/`, su `layout.json` y `tools/build.py`. Se conserva el paquete gráfico aportado, incluidos sus maestros y referencias. El README interno describe su estado offline v0.1; la integración vigente se documenta en `docs/QA11_INTEGRACION_LOGO.md`.

Con Pillow y NumPy instalados:

`python3 tools/integrate_title_assets.py JP.ws --out title_edits.json --report title_report.json --write-source`

El importador recompone los recursos desde los PNG editables, convierte mapas y patrones, comprueba el espacio asignado y reemplaza únicamente las entradas `TITLE_` de `src/corrections.json`. A continuación usar `build.py --development` para una edición intencional; verificarla antes de actualizar el hash de publicación. El generador `generate_title_fix.py` es histórico de HF7 y no representa el logo actual.

Consultar `INFORME_ES.md`, `manifest.json`, `docs/QA11_RUN_INDEX.json`, `docs/approval_matrix.json` y `CONTEXTO_CONTINUACION.md`. Los pendientes anteriores se mantienen en `docs/issue_register.json`.
'''
(root/'README.md').write_text(readme)
report=f'''CHOCOBO — HF8 TEST / QA11 — 14 de octubre de 2026

Resultado
Se integró el logo inglés entregado en Chocobo_WS_Logo_EN_v0.1_Fuentes_y_Animacion.zip. Se respetaron sus letras, proporciones, composición y píxeles nativos. El diseño reemplaza al rótulo provisional de HF7; utiliza la paleta real del juego.

La integración usa 139 patrones de 8×8 dentro del recurso nativo de 411 tiles. Se conservan los 64 tiles de animación de Chocobo y el código que controla poses, tiempos, copyright y PUSH BUTTON. Se recompusieron dos mapas; sus tamaños comprimidos son 247 y 625 bytes. No se introdujo un reproductor de GIF.

Validación realizada
• 1.001 cuadros comparados: filas 0–55 y 121–143 idénticas a HF7; cero discrepancias.
• En esos mismos cuadros, las filas 64–120 del nuevo rótulo/subtítulo coinciden píxel a píxel con el diseño aportado, usando los cuatro colores de la paleta nativa.
• Cuatro poses estables y transiciones visibles; copyright, parpadeo, menú, partida nueva y llegada al pueblo verificados desde arranque mediante botones. Movimiento posterior verificado desde el estado generado por ese recorrido.
• Reconstrucción desde los assets editables idéntica a los cambios incluidos; build desde JP y aplicación BPS independiente idénticos.
• 11 pruebas de infraestructura correctas. Cambios respecto a HF7: {m['changed_bytes_vs_hf7']} bytes, incluidos los dos bytes de checksum. Cero cambios fuera de recursos exclusivos del título y checksum; fixes de juego y guardado byte-idénticos.

Alcance de calidad
La lectura directa en pantalla fue revisada con conocimiento del texto. No se presenta como reconocimiento ciego ni se hereda el PASS de los 36 glifos del diseño anterior de HF7. La aprobación formal independiente de glifos del arte aportado queda pendiente; su fidelidad de integración está comprobada. No se redibujó el diseño del usuario.

HF8 sigue siendo TEST. Maquetación global, disparador del bloqueo por equipamiento y variante histórica del bloqueo de Atla conservan sus pendientes; esta fase no altera ni vuelve a certificar esas rutas. Tampoco se ejecutaron hardware real ni segundo emulador.

Identidad
JP SHA-256: {m['original']['sha256']}
HF8 SHA-256: {m['target']['sha256']}
HF8 CRC32: {m['target']['crc32']}; checksum WS: {m['target']['ws_checksum']}.
BPS SHA-256: {m['bps_sha256']}
Archivo gráfico aportado SHA-256: {m['user_logo_archive_sha256']}
Entorno: Linux x86_64, Mesen 2.1.1. Fuentes completas acumulativas, evidencias, estados y BPS directo desde JP. No se incluyen ROM, BIOS ni emulador.
'''
(root/'INFORME_ES.md').write_text(report);(delivery/'Informe_Chocobo_HF8_QA11_20261014.txt').write_text(report)
(root/'CHANGELOG.md').write_text('''# Changelog

## HF8 TEST — QA11 — 2026-10-14

- Integra el logo del paquete v0.1 entregado por el usuario en el renderer nativo.
- Conserva la animación original, copyright, prompt, menú y todos los fixes anteriores.
- Añade importador reproducible desde PNG editables, comparación de 1.001 cuadros y prueba de arranque hasta pueblo.
- Invalida la aprobación de glifos del título anterior; no declara aprobación visual global ni causa resuelta para bloqueos no reproducidos.

Historial anterior: `docs/history/hf7_qa10/CHANGELOG.md` y registros QA1–QA10 incluidos.
''')
(root/'CONTEXTO_CONTINUACION.md').write_text('''# Continuación tras HF8 / QA11

Autoridad actual: manifest.json y build.py de HF8. Logo vigente: assets/title/user_v01. Importador: tools/integrate_title_assets.py, desde la JP identificada. No volver a insertar el rótulo provisional HF7. Su generador y documentación quedan como historial.

El rótulo nuevo es idéntico a los píxeles aportados en filas64–120, con la paleta nativa. La animación original conserva sus64tiles y código; comparación de1.001cuadros. Nuevo juego y movimiento en pueblo completados. Procedencia de estados y hashes: docs/QA11_RUN_INDEX.json. No son pruebas de persistencia de guardado.

Pendiente artístico formal: reconocimiento independiente sin contexto de los glifos del logo aportado. La lectura directa realizada conocía el texto y no concede ese PASS. No modificar el arte seleccionado por el usuario sin un defecto concreto.

Pendientes heredados: maquetación global; causa de bloqueo por equipamiento (siguiente hipótesis útil: equipos fusionados/campo auxiliar, no repetir92consultas básicas); variante histórica del congelamiento de Atla. El rescate D2F60 y regreso ya tienen PASS sintético acotado en QA10. Ascensor continuo, ruta natural de teletransporte y causa natural de reset siguen según issue_register.json. Incidente físico eléctrico fuera del alcance ROM.

HF8 cambia sólo datos exclusivos del título y checksum respecto de HF7. No repetir pruebas cerradas de guardado, Lafoss o eventos sin un cambio o riesgo concreto. Ahorro de tokens no medido.
''')
(root/'docs/QA11_INTEGRACION_LOGO.md').write_text('''# Integración del logo aportado — QA11

## Base y procedencia

HF7 fue verificada por SHA-256 antes de continuar. La ROM HF8 reconstruida desde JP es byte-idéntica a la candidata usada en todas las pruebas QA11. Los nombres de ruta en run.json conservan la candidata `private_roms/qa11_title.ws`; su hash es el de la entrega final. La base y el archivo gráfico constan en manifest.json.

El ZIP de arte se conserva como fuentes expandidas en assets/title/user_v01. Sus documentos describen su estado previo offline, no el estado de integración HF8. Se mantiene autoría/procedencia y sus advertencias originales. La paleta RGB de su GIF no es una lectura de hardware; se usan sus índices con los cuatro colores del juego. La primera imagen offline no incluye copyright: el juego sí lo muestra y QA11 lo comprobó.

## Operación binaria

- Recurso nativo: ROM155155..156B04,411tiles 2bpp; consumidor154A27..154A43, destino WRAM2000.
- Reserva para arte: tiles61..194 y215..327 (247 disponibles); se usan139. Tiles328..391 de animación intactos;392..410 del japonés anterior vacíos.
- Mapa0 en150034..1501B6:247bytes comprimidos y padding FF. Paleta transparente4 conservada.
- Mapa1: puntero150032 a15FD58;625bytes, termina15FFC8 inclusive. Se respeta el código anterior en15FD00..15FD57.
- Formato nativo de mapas,1024words, compresión LZ del juego. Recompresión/decodificación exacta; preimágenes y presupuesto de tiles/mapa verificados.
- El arte usa filas56..120; la animación nativa sigue superpuesta en su ventana. La prueba de fidelidad del rótulo cubre64..120 inclusive. Copyright y PUSH BUTTON siguen siendo controlados por el juego.
- Checksum actualizado. No cambia la fuente compartida, la lógica de eventos, el guardado ni la lógica de equipamiento.

## Recorrido y evidencia

Comando reproducible, usando un Mesen2.1.1 privado:

`python3 qa11/run.py HF8.ws - qa11/title_animation.lua runs/title --timeout 35 --mesen /ruta/Mesen`

Planes title_menu.lua (2000frames), title_animation.lua (1400frames, capturas300..1300) y start_game.lua (4000frames). El estado de walk procede de start_game y utiliza post_ending_walk.lua,480frames; el nombre histórico del plan no convierte esta prueba en un ending. No se hacen pokes ni cambios de registros. Accesos SCRIPTED_NATURAL y SAVESTATE con botones.

Comparación: qa11/compare_animation.py y animation_validation.json. Los mapas registrados en1000 correspondían a BG1 y contienen la nueva ilustración fija: su desigualdad es esperada. No se usa ese registro como prueba de igualdad del mapa animado. Las pruebas válidas son igualdad de píxeles superiores/pie, estabilidad del logo, tiles de animación byte-idénticos y ausencia de cambios en el código nativo.

Los16estados superiores RGB incluyen cuatro poses estables y transiciones de la representación LCD del emulador; no se afirma que existan16poses. El GIF de entrega es una previsualización muestreada de capturas reales, no reemplaza los registros por cuadro ni controla el juego.

## Límites

No se transfiere la aprobación de36glifos de HF7 al diseño diferente de HF8. Lectura directa revisada; reconocimiento independiente sin contexto pendiente. Los estados previos QA1–QA10 mantienen su hash/procedencia y no se presentan como nuevas ejecuciones de HF8. Su vigencia se limita a código/recursos no modificados; los pendientes anteriores permanecen explícitos.
''')
(root/'docs/QA11_VALIDATION_SUMMARY.json').write_text(json.dumps({'unit_tests':{'passed':11,'failed':0},'editable_assets_regeneration':'EXACT_EDITS_MATCH','independent_bps':'EXACT_TARGET_MATCH','runtime_build_sha256':m['target']['sha256'],'native_pixel_frames_compared':1001,'unexpected_changed_offsets':0,'new_game':'SCRIPTED_NATURAL_PASS_TO_VILLAGE','walk':'SAVESTATE_FROM_NATURAL_ROUTE_PASS','hardware':'NOT_VALIDATED','second_emulator':'NOT_VALIDATED','formal_independent_glyph_review':'NOT_VALIDATED'},indent=2)+'\n')
print('HF8 documents and distributed BPS updated')
