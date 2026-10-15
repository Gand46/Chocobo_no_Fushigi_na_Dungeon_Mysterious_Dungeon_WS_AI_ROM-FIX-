from pathlib import Path
import json,csv,shutil

root=Path('delivery/Chocobo_EN_v1.1_HF5_TEST_Fuentes_QA8_20261014')
m=json.loads((root/'manifest.json').read_text())
report='''# Chocobo — HF5 TEST / QA8

Continuación del 14 de octubre de 2026, UTC. Traducción japonesa → inglés. Compilación experimental, no RC. Se incorporan tres correcciones concretas: proyectil de Lafoss, acceso al daño nativo de las dos últimas perlas y un terminador de texto adicional. Son seis bytes de contenido y un byte de checksum respecto a HF4.

## Estado de los ocho pendientes

| Frente | Resultado de esta iteración | Pendiente concreto |
|---|---|---|
| Maquetación global, TR-01 | Corregida una lectura fuera del espacio de una cadena. Censo de 2.333 entradas en 19 familias: un candidato antes, cero después | Aprobación visual del resto de diálogos, tiendas, créditos y eventos; el censo no cubre todo el guion ni mide anchura global |
| Título japonés, TR-03 | Identificados consumidor y 411 tiles nativos; extraídos los recursos editables | Diseñar e integrar el título inglés conservando el estilo original; sigue japonés |
| Equipamiento, EN-01 | Cuatro casos adicionales de descripción con bolsa de 18 objetos y nivel +99, incluido el último espacio, sin bloqueo ni escrituras persistentes observadas | Reproducir el disparador natural y determinar su causa; no hay fix nuevo de equipamiento |
| Lafoss, EN-02 | PASS sintético de la acción nativa Kick: proyectil, impacto de 1.000 puntos con defensa cero, muerte del enemigo, consumo y continuación | Otras combinaciones de combate, adquisición natural y hardware no están aprobados; el caso Kick reproducido sí queda corregido |
| Pisos/ascensor, JP-01 | Ampliados los pisos sintéticos. La carga del 99 queda blanca también en JP con la misma fixture mínima; el bloque de datos se copia íntegro | Aislar la condición de reconstrucción del evento y probar el ascensor real antes de modificar código |
| Segundo final y fuente/rana, JP-02 | PASS sintético de la ruta base: jefe asistido, créditos, escenas del pueblo y desplazamiento normal posterior | Comparar la ruta con la fuente limpia y la rana invocada antes de finalizar D2; ese fallo no queda corregido |
| Teletransporte 99→30, JP-03 | Identificada Telep Card, ID 0B; obtenidos estados D3 posteriores al segundo final, incluidos 98 y 30 | Conseguir el 99 por una transición trazable, usar Telep Card y regresar al 30; la secuencia exacta sigue sin validar |
| Rescate de Atla, JP-04 | Avanzada una secuencia de D1 F30 hasta volver al pueblo | Identificar y reproducir el rescate concreto; no se equipara cualquier escena de D1 al incidente de Atla |

## Correcciones implementadas

Lafoss tenía dos fallos distintos. El selector del proyectil enviaba el objeto FF a una entrada FFFF sin modelo. HF5 asigna el modelo de perla 0AF8 usado por los objetos vecinos. La comprobación exhaustiva de los 256 IDs demuestra que solo cambia FF. Se conserva la protección de HF2 como respaldo.

La rutina de daño excluía FE y FF mediante un límite superior FE. Sin embargo, el inicializador contempla las 16 perlas F0–FF y el juego ya contiene un cálculo de 1.000 puntos para FE/FF. HF5 amplía el límite a 100 hexadecimal: activa esa implementación existente, sin insertar un daño inventado. La traza pasa de un valor residual de 3 a 1.000; con defensa 200 aplica 800, y con defensa 2.000 aplica 1 según el código nativo. La prueba FE también pasa de 3 a 1.000. No se generaliza una cifra fija a todas las defensas.

La entrada 81 de la familia 0 había perdido FFFF. Se restaura dentro de sus ocho bytes originales. El consumidor ahora lee cuatro palabras, frente a cinco que alcanzaban la siguiente entrada. Las capturas son idénticas: se conserva la etiqueta visible «3». Es una corrección de límites, no una demostración de un desbordamiento visible.

## Validación y límites

Se ejecutó Mesen 2.1.1 en Linux. Las pruebas de inventario, recursos y eventos usan estados e inyecciones explícitas. El segundo final parte del estado D2 sintético de QA7; para superar el combate se redujo la vida del jefe a 1 y se mantuvo la del personaje en 500. Después se siguieron las escenas con entradas normales, sin saltar instrucciones del evento. Las capturas y cambios de guion documentan créditos, pueblo y movimiento posterior. Esto no valida todavía la variante fuente/rana descrita en el foro.

La fixture D3 antigua necesitaba la máscara 0080, no 8000, igual que D2. La corrección de esa fixture mejora la investigación y no es un cambio de ROM. Algunas pantallas blancas persisten; no se consideran prueba de corrupción del bloque guardado. Los estados con progreso insuficiente incluso devolvían el piso 30 al pueblo; al usar el progreso producido por el segundo final se carga un piso 30 visible. Por eso no se da por probada la causa del foro con una fixture incompleta.

HF5 conserva byte a byte el código de guardado HF4. Se realizó un guardado nativo nuevo y una carga en proceso nuevo: nivel 3, HP 28, los 2.516 bytes del bloque recuperados exactamente. Las matrices HF4 de 7.606 prefijos y 144 mutaciones se conservan como evidencia histórica del mismo código, no como pruebas repetidas en esta iteración. No hay recuperación automática del bloque anterior ni identificación de la causa natural de los resets.

Build directo desde JP, reaplicación con aplicador BPS independiente, checksum y 11 pruebas de infraestructura: PASS. El caso de equipamiento 93/espacio 9 seleccionó otro objeto y se excluye del conteo de cuatro casos válidos. La sonda Flare no alcanzó al enemigo y no cuenta como regresión de daño aprobada. Un primer intento de guardado apuntó a un archivo inexistente; se descarta y se sustituye por q8_save_final/q8_cold_saved.

La maquetación global, el título, fuente/rana, ascensor, teletransporte, Atla, segundo emulador y hardware siguen abiertos. El fallo eléctrico del cartucho permanece cerrado y fuera del alcance de la ROM.

## Aplicación y compatibilidad

Aplicar el BPS HF5 directamente a la ROM japonesa limpia de 2.097.152 bytes, CRC32 CCAA4853. No encadenarlo sobre HF4. Se incluyen todas las correcciones anteriores y los fuentes editables reconstruidos; no son el código fuente original del juego. No se distribuyen ROM ni BIOS.

HF5 comparte el formato de guardado protegido HF4. Carga partidas antiguas y las protege al guardar; para volver a JP/EN/HF1–HF3 se debe exportar una copia con tools/chocobo_save.py --export-legacy. Las versiones anteriores no reconocen directamente la cabecera protegida. El exportador verifica integridad y no sobrescribe el original. Mantener una copia del guardado al probar esta versión TEST.

Referencias externas de los casos, tratadas como testimonios y no como demostraciones del código:
- https://wazap.com/cheat/セーブデータ破損？バグ/570082/ — pisos, ascensor y comentario de teletransporte.
- https://wazap.com/cheat/クリア不能バグと対処法/570080/ — segundo final y fuente/rana.
- Chat compartido revisado en QA6: https://chatgpt.com/share/6acebdec-2b5c-83e9-833e-60560c52d788
'''
hashes=f'''\n## Identificación exacta\n\nJP SHA-256: {m['original']['sha256']}\nHF5 SHA-256: {m['target']['sha256']}\nHF5 CRC32: {m['target']['crc32']}; checksum WS: {m['target']['ws_checksum']}\nBPS SHA-256: {m['bps_sha256']}\n'''
(root/'INFORME_ES.md').write_text(report+hashes)
Path('delivery/Informe_Chocobo_HF5_QA8_20261014.txt').write_text(report+hashes)
readme='''# Chocobo English v1.1 + HF5 TEST

Compilación experimental, no RC. Incluye HF1–HF4 y tres fixes de QA8: proyectil Lafoss, acceso al daño nativo de las perlas FE/FF y terminador de la familia 0, entrada 81. Sigue pendiente la aprobación global. El título continúa japonés.

Aplicar patches/Chocobo_EN_v1.1_HF5_TEST_JP_CCAA4853.bps directamente a JP CCAA4853, sin parches previos. Alternativamente:

```sh
python3 build.py /ruta/JP.ws --out build
python3 -m unittest discover -s tests -v
python3 tools/verify_evidence.py /ruta/JP.ws
python3 tools/verify_independent_bps.py /ruta/JP.ws
python3 qa8/text_census.py /ruta/JP.ws build/Chocobo_EN_v1.1_HF5_TEST.ws --out census
```

El build requiere Python 3 y no incluye ROM ni BIOS. src/corrections.json conserva precondiciones exactas. Los recursos anteriores y la protección de guardado se integran acumulativamente. El ensamblador de la protección está en src/save_guard.s. Estos fuentes reconstruyen la traducción/parche, no el fuente original del juego.

HF4/HF5 comparten partidas protegidas. Para versiones anteriores, exportar una copia legacy verificada:

```sh
python3 tools/chocobo_save.py partida.sav
python3 tools/chocobo_save.py partida.sav --export-legacy copia_legacy.sav
```

Usar SRAM cruda de 32 KiB, no savestates. Las partidas legacy no tienen CRC retrospectivo. La protección rechaza un bloque incompleto; no recupera automáticamente una partida sobrescrita. Conservar una copia antes de probar esta versión TEST.

Estado vigente: INFORME_ES.md, docs/issue_register.json y docs/quality_gates.json. Reproducción QA8: docs/QA8_REPRODUCTION.md. Capturas y savestates: evidence/qa8_runs. Los documentos de docs/history describen builds anteriores y no sustituyen el estado HF5.
'''
(root/'README.md').write_text(readme+hashes)
(root/'CHANGELOG.md').write_text('''# HF5 TEST / QA8 — 2026-10-14 UTC

- Restaura el proyectil nativo 0AF8 para Lafoss FF.
- Corrige el límite superior que omitía el daño ya implementado para FE/FF.
- Restituye un terminador FFFF en familia 0, índice 81, sin cambio visual.
- Completa sintéticamente la ruta base del segundo final, hasta caminar por el pueblo.
- Amplía evidencia de textos, bolsa llena, pisos D3 y guardado nativo/carga fría.
- Extrae los tiles nativos del título como insumo; no traduce todavía su gráfico.
- Conserva todos los fixes HF1–HF4 y el formato de guardado HF4.

Siete bytes distintos respecto a HF4, contando el checksum. La compilación sigue siendo TEST. Historial HF4: docs/history/hf4_qa7.
''')
issues=json.loads((root/'docs/issue_register.json').read_text())
updates={
'TR-01':('PARTIAL_HF5_TERMINATOR_FIXED','11 resources corrected cumulatively; 2333 entries/19 native families have zero JP-terminated/EN-unterminated candidates after fix. Not global layout approval.'),
'TR-03':('RESOURCE_EXTRACTED_UNTRANSLATED','Native title tiles155155..156B04 and loader154A27 identified; English artwork/integration pending.'),
'EN-01':('NOT_REPRODUCED_BOUNDED','Four new full-bag +99 description cases valid; no guarded text-buffer overrun or persistent-block write observed. Slot9/id93 excluded: wrong selection. Natural cause remains unknown.'),
'EN-02':('FIXED_SYNTHETIC_NATIVE_KICK','FF projectile restored; FE/FF native damage enabled; FF enemy death, consumption and return confirmed. Damage1000 with defense0,800 with200,1 with2000. Other combat contexts/natural acquisition not globally approved.'),
'JP-01':('PARTIAL_SYNTHETIC_INVESTIGATION','D3 mask0080 corrected in fixtures; event-floor white screen persists, including JP control at99. Cold-copy payload exact. Actual elevator route/root cause unproven.'),
'JP-02':('BASE_ENDING_PASS_SYNTHETIC_FOUNTAIN_BRANCH_PENDING','Assisted boss defeat -> credits -> village scenes -> native walking. Fountain/frog-before-ending variant not validated and not fixed.'),
'JP-03':('NOT_VALIDATED_ROUTE','Telep Card ID0B identified on native UI. Post-ending D3 states98/30 obtained; exact99->Telep->30 route pending.'),
'JP-04':('NOT_VALIDATED_RESCUE','D1 floor30 sequence returned to village; not identified as the specific Atla rescue incident.'),
}
for r in issues:
 if r['id'] in updates:r['status'],r['scope']=updates[r['id']]
 if r['id']=='SAVE-01':r['scope']+='; HF5 native new write and cold load exact2516bytes PASS; guard code unchanged.'
(root/'docs/issue_register.json').write_text(json.dumps(issues,indent=2)+'\n')
with (root/'docs/issue_register.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['id','status','scope']);w.writeheader();w.writerows(issues)
g=json.loads((root/'docs/quality_gates.json').read_text());g.update(version='HF5_TEST',save_protected_normal_load='PASS_HF5_NATIVE_WRITE_COLD_BOOT_EXACT_PAYLOAD',save_write_prefixes='INHERITED_HF4_IDENTICAL_CODE_7606',save_crc_mutations='INHERITED_HF4_IDENTICAL_CODE_144',lafoss_no_hang='PASS_SYNTHETIC_HF5',lafoss_full_spell_semantics='PASS_SCOPED_NATIVE_KICK_PROJECTILE_DAMAGE_CONSUMPTION_ENEMY_DEATH',lafoss_all_combat_contexts='NOT_VALIDATED',late_events='BASE_SECOND_ENDING_PASS_SYNTHETIC_OTHER_BRANCHES_PENDING',text_terminator='PASS_NATIVE_CONSUMER_BOUNDARY_AND_IDENTICAL_PIXELS',text_global_layout='NOT_VALIDATED',title_translation='NOT_VALIDATED_UNTRANSLATED',fountain_frog_before_ending='NOT_VALIDATED',teleport99_to30='NOT_VALIDATED',atla_rescue='NOT_VALIDATED')
(root/'docs/quality_gates.json').write_text(json.dumps(g,indent=2)+'\n')
approval={
'scope':'HF5 three binary corrections; overall release TEST',
'DISCOVERED':'PASS_NATIVE_DATA_CODE_AND_RUNTIME',
'TRANSLATED':'N/A_NO_NEW_ENGLISH_WORDING_TITLE_REMAINS_UNTRANSLATED',
'INTEGRATED':'PASS_PREIMAGES_AND_ALLOWED_DIFF',
'RUNTIME_CONFIRMED':'PASS_SCOPED_SYNTHETIC_MESEN',
'LINGUISTIC_APPROVED':'N/A_NO_NEW_WORDING_GLOBAL_PENDING',
'TYPOGRAPHY_APPROVED':'PASS_SCOPED_UNCHANGED_NUMERIC_LABEL_NO_FONT_EDITS',
'LEGIBILITY_APPROVED':'PASS_SCOPED_LABEL_AND_COMBAT_CAPTURES',
'DESIGN_APPROVED':'PASS_SCOPED_REUSE_OF_NATIVE_PEARL_MODEL_AND_NATIVE_DAMAGE',
'VISUAL_APPROVED':'PASS_SCOPED_PROJECTILE_DAMAGE_LABEL_GLOBAL_PENDING',
'FUNCTIONAL_APPROVED':'PASS_SCOPED_KICK_AND_TEXT_BOUNDARY_NATIVE_SAVE_COLD_LOAD',
'FINAL_APPROVED':False,
'reason':'Global layout/title, fountain branch, actual elevator/teleport/Atla routes and hardware unvalidated.'}
(root/'docs/approval_matrix.json').write_text(json.dumps(approval,indent=2)+'\n')
continuity='''# Continuidad HF5 TEST / QA8

Último build SHA256 312f688f627f0c5ccf430c35c9632033344fc0397aa25c6f0db9d99a3630f9c8, CRC3887C0CF, checksum06CA. BPS directo desde JP CCAA4853; no encadenar HF4.

Lafoss: modelo faltante corregido1422C5 FFFF→0AF8; daño FE/FF habilitado1EA771 FE00→0001. La rutina14CA16/14CBB3 ya implementaba daño base1000. El menú nativo usa Kick, no un comando llamado Use. Terminal familia0/81 restaurado16E6FA0000→FFFF. Guardado HF4 permanece idéntico.

Prioridad siguiente: fuente/rana antes de concluir D2 y reconstrucción de pisos/ascensor. D2 ya pasó créditos y vuelve al control: evidence/qa8_runs/q8_d2_walk/checkpoint.mss. Estado sintético, jefe HP1 y personaje HP500 durante combate. No llamarlo progresión natural. Para bifurcar antes del final usar q8_d2_event_progress2 (jefe vivo) o q8_d2_boss_assist (postjefe antes de créditos); el segundo requiere demostrar que los flags de fuente se consultan después de ese punto. Rana/Frog Card ID04; Geyser Card ID09; Telep Card ID0B, identificados visualmente. Falta mapear los flags de la misión, no asumir que basta con inyectar las cartas.

D3 con progreso del final: q8_D3_post_ending_to_98 es campo98, q8_D3_post_ending_to_30 es campo30 y99 queda blanco. La fixture mínima anterior usaba730A8000 por error: el bit es0080. D3 requiere730C bit4, pero esos dos bits no reconstruyen toda la historia. Conservar datos exactos y separar corrupción persistente de carga de evento. No reabrir el bloqueo eléctrico del cartucho.

Título: qa8/title_assets tiene411tiles2bpp nativos, ROM155155..156B04, loader154A27. Aún japonés. Mantener estilo; no sustituir por una fuente genérica.

Equipamiento: cuatro nuevos Check +99 con18objetos, IDs65/9D/BF/C0, sin fallo. El intento93/slot9 abrió otro objeto y está excluido. No constituye causa resuelta. Atla tampoco: D1F30 volvió al pueblo, pero no se ha vinculado al rescate preciso.

No repetir matrices de guardado QA7 sin cambio de código. Guardar nativamente y cargar en frío para persistencia; savestates solo validan su ruta. Consultar informe y QA8_REPRODUCTION; los archivos históricos pueden contener conclusiones superadas, expresamente versionadas.
'''
(root/'CONTEXTO_CONTINUACION.md').write_text(continuity)
print('HF5 documentation written')
