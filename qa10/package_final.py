from pathlib import Path
import json,shutil,hashlib,csv,struct
from PIL import Image,ImageDraw,ImageFont
root=Path('delivery/Chocobo_EN_v1.1_HF7_TEST_Fuentes_QA10_20261014');m=json.loads((root/'manifest.json').read_text());br=json.loads(Path('private_roms/hf7_delivery_build/build_result.json').read_text());m['bps_sha256']=br['bps_sha256'];(root/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
bpsname='Chocobo_EN_v1.1_HF7_TEST_JP_CCAA4853.bps'
for dst in [Path('delivery')/bpsname,root/'patches'/bpsname]:shutil.copy2(Path('private_roms/hf7_delivery_build')/bpsname,dst)
issues=json.loads((root/'docs/issue_register.json').read_text())
updates={'TR-01':('PARTIAL_92_ITEM_DESCRIPTION_SURFACES','92 IDs65..C0 tested through native Check:90 named items,2 empty reserved entries9B/9C. TitanSaddle residual w fixed at16F1D4. No global layout or linguistic approval.'),'TR-03':('ENGLISH_TITLE_INTEGRATED_RUNTIME_PASS','Title, platform caption, animation and title-menu transition verified. Canonical stencils, two native maps and 411-tile resource preserved structurally. Animation tiles328..391 unchanged.'),'EN-01':('NOT_REPRODUCED_92_BASE_ID_CHECKS','All92 description getters observed; no crossings in two watched text stores and no writes to175AC..17F8F. Synthetic bag records. Cause of reported freeze remains unknown; fusion combinations and exact failing save remain pending.'),'JP-04':('PASS_SCOPED_SYNTHETIC_EXACT_PREBOSS_SCENE','D2F60 pre-boss rescue traced E0:9A1C..9E4D, transformations/extraction9D07 onward, flag18 set at9E44. No pointer injection or memory edits in rescue plan. Boss then assisted; ending and village movement completed. Retrospective Yahoo failure conditions unknown; no Atla binary fix.')}
for it in issues:
 if it['id'] in updates:it['status'],it['scope']=updates[it['id']]
(root/'docs/issue_register.json').write_text(json.dumps(issues,indent=2)+'\n')
with (root/'docs/issue_register.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=['id','status','scope']);w.writeheader();w.writerows(issues)
q=json.loads((root/'docs/quality_gates.json').read_text());q.update(version='HF7_TEST',title_translation='PASS_RUNTIME_ENGLISH',title_glyph_review='PASS_NATIVE_SURFACE_PLUS_36_ISOLATED_GLYPHS',atla_rescue='PASS_SCOPED_SYNTHETIC_PREBOSS_SCENE',equipment_cause='NOT_REPRODUCED',text_global_layout='PARTIAL_92_NATIVE_CHECK_SURFACES_GLOBAL_NOT_VALIDATED',text_terminator='PASS_TITAN_SADDLE_NATIVE_NAME_CONSUMER',final_approved=False);(root/'docs/quality_gates.json').write_text(json.dumps(q,indent=2)+'\n')
(root/'docs/approval_matrix.json').write_text(json.dumps({'scope':'HF7 title and TitanSaddle; QA10 equipment and Atla','DISCOVERED':'PASS','TRANSLATED':'PASS_TITLE','INTEGRATED':'PASS','RUNTIME_CONFIRMED':'PASS','LINGUISTIC_APPROVED':'PASS_TITLE_AND_TITAN_ONLY','TYPOGRAPHY_APPROVED':'PASS_SCOPED_TITLE_EXTENSION_NATIVE_PIXEL_GRID','LEGIBILITY_APPROVED':'PASS_SCOPED_NATIVE_VIEW_AND_ISOLATED_GLYPHS','DESIGN_APPROVED':'PASS_SCOPED_TITLE_HIERARCHY_ANIMATION_SEPARATION','VISUAL_APPROVED':'PASS_SCOPED','FUNCTIONAL_APPROVED':'PASS_SCOPED_SYNTHETIC_RESCUE_AND_MENU','FINAL_APPROVED':False,'pending':'Global layout/linguistics; equipment historical trigger; exact Yahoo failure variant; other inherited pending issues.'},indent=2)+'\n')
repro='''# QA10: reproducción y alcance

HF7 es TEST, no RC. Build actual y BPS identificados en manifest.json. Python3 para build; Pillow sólo para hojas de inspección. Mesen2.1.1 Linux x86_64 SHA256 ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41. No se redistribuye ROM, BIOS ni emulador.

## Título

El cargador154A27 copia411tiles2bpp desde155155..156B04 a WRAM2000. Mapas nativos: descriptorC0 BG1800, base3C; descriptorC4 BG1000, baseC2. El mapa0 se recompone en150034..1501B6; puntero150032 dirige mapa1 a15FD58. Compresión nativa LZ, ver generate_whistle_fix.decode/encode. Todas las escrituras exigen preimagen y no solapan Walking15FD00. La animación usa tiles328..391 y una ventana6x6 que termina en y63. Se conservan esos64tiles y el dibujo superior; letras grandes comienzan y65. Una candidata y60 fue rechazada porque la animación pisaba algunas letras. La capa BG2 conserva la paleta transparente4; una candidata sin ese bit fue rechazada por banda negra.

Texto: CHOCOBO'S / MYSTERY DUNGEON / FOR WONDERSWAN. Extensión gráfica propia del logotipo: contorno negro, cara clara, sombra y cuadrícula de píxeles nativos; rótulo pequeño sólido con jerarquía de PUSH BUTTON. No se usa una fuente de sistema ni se cambia la fuente compartida de diálogos. Referencia nativa: evidence/qa8_runs/q8_title_reference y qa8/title_assets. Fuente editable: tools/generate_title_fix.py y assets/title/canonical_glyphs_and_layout.json. Regeneración opcional desdeHF6: python3 tools/generate_title_fix.py HF6.ws --out title_edits.json --source-out title_source.json. El build normal usa src/corrections.json y no requiere HF6.

Revisión de glifos: qa10/glyph_sheet.py extrae capturas reales con etiquetas numéricas. Las primeras pruebas registraron O parcialmente sobrescritas, N/A pequeñas ambiguas; se corrigieron posición, separación, contraforma y rótulo pequeño. glyph_review_initial.json conserva el fallo inicial. glyph_review_final.json documenta36lecturas; vista nativa completa y zoom2x diagnóstico. OCR no utilizado.

## Equipamiento y maquetación

qa10/equipment_suite/run_suite.py ROM ESTADO OUT --mesen MESEN --suite equipment --timeout220. Estado inicial q3_dungeon SHA2cb9e29b3749ce0caf9628ff93f8c5b52ebe5eb7212627175290a38d9adb5f82. Se reemplaza una ficha de bolsa por{1,ID,0,0,0}. IDs65..C0:92consultas;90objetos con nombre y2entradas vacías9B/9C. Para cada caso se confirmó family2/indexID en text_reads.csv, abrir Check y salir con B. Son SYNTHETIC_STATE más entradas nativas, no adquisición natural. El watcher vigila únicamente37AFF/37B7D con DI>=23C y el bloque persistente175AC..17F8F: no cubre toda la memoria ni todas las combinaciones de equipo fusionado.

TitanSaddle corresponde family3/indexA4, slot16F1CA..16F1D7. Palabras0342 0279 0343 0005 0310 0078 FFFF. El0078 es la w sobrante y pasa aFFFF; elFFFF siguiente queda como relleno. El menú real confirma TitanSaddle. La sospecha de recorte de GilTalon en la hoja de conjunto se descartó al abrir la captura individual: el texto completo cabe; no se modifica.

No confundir estas90descripciones con todas las ventanas del juego ni con sus páginas de propiedades. El bloqueo EN01 no se reprodujo. Próxima investigación útil: fichas de equipo fusionado y su estructura auxiliar, con un guardado que reproduzca el fallo; evitar repetir los92casos básicos.

## Atla: escena concreta y límites

Estado previo q7_d2_dialogue_progress SHA6d67f049fe57904e6b2de8578de2e651d9f50fba2eb485fc098c2a37adde7ed0, derivado de la fixture sintética D2F60 documentada en QA6. qa10/atla_rescue_final.lua sólo envía A, captura y observa: no escribe memoria, no altera punteros y no reduce HP. Ruta E0:9927..9E4D, con transición9A1C, transformación9AC9..9BD5, cambio de escena9CD0, personajes9D07/9D0D, transformación9D65..9E0F, salida9E3A/9E3D, bandera global18 activada por opcode70 en9E44. Al final: D2,piso60,730C pasa80→81 y comienza el combate. Capturas y estados de9D07/9E44 permiten retomar exactamente ese tramo. No es la escena de D1F30.

Cadena q10_final_atla_rescue -> q10_final_atla_boss -> q10_final_atla_ending -> q10_final_atla_walk. La segunda etapa sí usa asistencia explícita: HPjefe5A32=1 y HP/máximo jugador500, mantenimiento cada60frames. La escena de rescate se completó antes de aplicar esa ayuda. Créditos, pueblo y movimiento posterior documentados. El máximo524 posterior procede del desarrollo del juego, no de una nueva afirmación de guardado.

La variante retrospectiva que congelaba según Yahoo sigue sin pasos exactos. La escena ensayada pasa, pero eso no corrige ni descarta aquel fallo. No hay modificación binaria de Atla. Se cotejan iguales enJP/HF7 los guiones009900..009EFF, el creador de actores14DD50..14DDB5 y el manejador de banderas140000..14008B. El blog de juego consultado sobreD2 aporta orientación narrativa y es dePS; no acredita el comportamiento deWS.

## Reutilización entre candidatas

run.json fija los hashes de cada ejecución. La matriz92 usa53f7309816536ac970f5fe5e02b6e2e2e9d358e5367ce9786450a7d3701d5f78. La cadena completa Atla usa31d1a3ddeccb2aaf58c2e903aadf6390c2a36ccfe81a2f31c37c0d156bd4c681. La entrega final cambia respecto de esa candidata únicamente mapas/tiles exclusivos del título y checksum. Código, textos de eventos, TitanSaddle y guardado son idénticos; se reutiliza esa evidencia con este límite explícito. q10_release_title_verified y q10_release_items_verified usan la ROM final. No se transfiere una aprobación global.

q10_atla_rescue fue un fallo del observador: createSavestate desde endFrame bloqueó la captura al llegar al primer hito. Se corrigió al registrar un callback de ejecución de un solo uso. No cuenta como bloqueo del juego. q10_atla_rescue2/3 y final_atla_rescue son los controles corregidos. Otras candidatas de título se conservan como diagnóstico, no como entrega.
'''
(root/'docs/QA10_REPRODUCTION.md').write_text(repro)
report=f'''CH O C O B O — HF7 TEST / QA10 — 14 de octubre de 2026

Cambios reales
• Título traducido al inglés: CHOCOBO'S MYSTERY DUNGEON / FOR WONDERSWAN. Conserva el arte superior y los64tiles de animación. Se corrigieron la interferencia de la animación, el espaciado y la legibilidad de glifos pequeños detectadas durante QA.
• TitanSaddle: eliminada una w sobrante en el nombre mediante el terminador correcto, sin tocar la fuente ni el objeto.

Validación de los cuatro pendientes
Título: integrado y visible; animación,36glifos aislados y transición al menú revisados.
Maquetación: revisión acotada de92IDs de equipamiento (90objetos y2reservados), con trazas del consumidor real; TitanSaddle corregido. La maquetación global sigue pendiente.
Equipamiento:92consultas nativas Check y salida completadas. Ningún cruce en los dos stores vigilados ni escritura al bloque persistente. No se encontró el disparador del bloqueo histórico; no se añade un fix especulativo.
Atla: identificada y recorrida la escena previa al jefe deD2F60, E0:9A1C..9E4D, extracción/transformaciones9D07..9E0F y bandera18 en9E44. PASS sintético de esta ruta. Rescate sin pokes; combate posterior asistido, créditos, regreso y movimiento verificados. La variante exacta del testimonio de congelamiento sigue sin reproducirse y no se modificó su código.

Build
JP SHA256: {m['original']['sha256']}
HF7 SHA256: {m['target']['sha256']}
CRC32: {m['target']['crc32']}; checksumWS: {m['target']['ws_checksum']}.
Cambios frente aHF6: {m['changed_bytes_vs_hf6']} bytes, incluido checksum.
BPS SHA256: {br['bps_sha256']}
BPS directo desde JP CCAA4853, reconstrucción reproducible, comparación exacta y aplicador independiente.11pruebas de infraestructura. Emulador Mesen2.1.1, Linuxx86_64. No prueba en hardware ni segundo emulador.

Límites y continuidad
Sigue siendo TEST. No hay aprobación global. Los92casos y la cadena Atla conservan el hash de su candidata; el último ajuste sólo cambia gráficos/mapas del título y checksum. La fuente y el código de esos consumidores permanecen idénticos; el paquete justifica esa reutilización y contiene pruebas finales de título/TitanSaddle.
No se reabrieron aquí ascensor/teletransporte/fuente-rana; sus límites deQA9 se mantienen. El fallo eléctrico del cartucho continúa cerrado fuera del alcance ROM.

Fuentes externas consultadas
https://retroachievements.org/game/16362 — testimonio de Chauckles sobre Check/equipamiento, sin objeto ni guardado preciso.
https://retroachievements.org/forums/topic/14392 — aviso general de congelamiento/guardado y revisiónJP.
https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14305291199 — inaccesible; se conserva la reseña histórica, no una nueva verificación.
https://sekaijyusaya.hatenablog.com/entry/2026/05/03/002434 — orientación narrativa deD2; imágenes dePS, no evidenciaWS.

Consultar docs/QA10_REPRODUCTION.md y QA10_RUN_INDEX.json para comandos, estados, hashes y exclusiones. Fuentes completas acumulativas; no contiene ROM, BIOS ni emulador. Ahorro de tokens: no medido.
'''
Path('delivery/Informe_Chocobo_HF7_QA10_20261014.txt').write_text(report)
(root/'INFORME_ES.md').write_text(report)
(root/'README.md').write_text('# Chocobo English v1.1 + HF7 TEST\n\nTítulo inglés y TitanSaddle corregidos; conserva todos los fixes anteriores. No es RC/final.\n\nConstrucción: `python3 build.py JP.ws --out build` (Python3, sin dependencias externas). Aplicar patches/'+bpsname+' a JP CCAA4853; no requiere cadena de parches.\n\nConsultar manifest.json, INFORME_ES.md, docs/QA10_REPRODUCTION.md y docs/issue_register.json. No incluye ROM/BIOS/emulador.\n')
(root/'CHANGELOG.md').write_text('# HF7 TEST / QA10\n\nTítulo inglés en el formato nativo, con animación conservada y coordenadas corregidas; TitanSaddle termina antes del glifo residualw. Matriz92 Check; rescate D2F60 concreto y recorrido posterior. No fix especulativo de equipamiento oAtla.\n\n'+(root/'CHANGELOG.md').read_text())
(root/'CONTEXTO_CONTINUACION.md').write_text('''# Continuación tras HF7 / QA10

Build y BPS en manifest.json; fuentes acumulativas. No repetir la matriz92 sin hipótesis nueva. Título ahora inglés, con letras grandes desdey65 para evitar la animación nativa que alcanza y63. Map1 reubicado15FD58; generador tools/generate_title_fix.py, canon assets/title. TitanSaddle:16F1D4 7800→FFFF.

Maquetación sigue globalmente pendiente; se han revisado90nombres/descripciones de equipo y2entradas reservadas. EN01 no reproducido: siguiente objetivo útil son equipos fusionados y su campo auxiliar, no más variantes equivalentes del mismo Check básico. Vigilancia actual sólo dos stores de texto y175AC..17F8F.

Atla: rescate antes del jefeD2F60, guion9A1C..9E4D; hito9D07 y bandera18 en9E44. Estado previo q7_d2_dialogue_progress; estados puntuales en q10_final_atla_rescue. Plan sin pokes. La cadena continúa con combate asistido, créditos y control en pueblo. Escena PASS sintética; disparador del congelamiento retrospectivo no reproducido. No atribuir el fallo del observador createSavestate/endFrame al juego.

Última revisión del título cambia sólo recursos exclusivos del título y checksum frente a31d1a3...; guiones, equipo y guardado idénticos justifican reutilización de evidencia. Todos los hashes figuran en el índice. Ascensor continuo, teletransporte natural, fuente/rana original, causa natural del reset y cobertura global conservan sus pendientes deQA9. Incidente físico eléctrico cerrado.
''')
print('Docs and BPS ready')
