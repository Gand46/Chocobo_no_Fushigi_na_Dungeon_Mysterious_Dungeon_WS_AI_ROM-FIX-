from pathlib import Path
import json,hashlib,datetime,shutil,base64,html
R=Path('delivery/Chocobo_EN_v1.1_HF13_TEST_Fuentes_QA18_M4_20261014');Q=Path('qa18');v=json.loads((Q/'verification.json').read_text());cov=json.loads((Q/'coverage_summary.json').read_text());ed=json.loads((Q/'edits.json').read_text());m=json.loads((R/'manifest.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m['qa18']={'status':'M4_EXECUTED_PASS_SYNTHETIC_SCOPED','new_corrected_unique_resources':5,'approved_scoped_runs':7,'diagnostic_runs':23,'approved_native_frames':7500,'checks':259,'visual_readings':14,'content_changed_bytes':147,'checksum_changed_bytes':2,'global_layout_approved':False,'global_linguistic_approved':False,'remaining_base_iterations':0,'unconfirmed_context':'TR-01-M2-C01 preset32/F00:I053','inheritance':cov['inheritance_rule'],'historical_qa17_checks_rerun':790,'unit_tests_passed':11};m['layout_iteration']['status']='FOUR_ITERATIONS_EXECUTED_GLOBAL_VISUAL_REVIEW_INCOMPLETE';(R/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
reg=[x for x in json.loads((R/'docs/issue_register.json').read_text()) if not x['id'].startswith('M-18-') and x['id']!='TR-01-L-G06-M073']
for x in reg:
 if x['id']=='TR-01-M':x.update(status='M4_EXECUTED_SCOPED_PASSES_GLOBAL_NOT_APPROVED',scope='M4/HF13: five message resources corrected, seven final synthetic runs,147 content bytes+2 checksum. No remaining vertical static candidates; three horizontal alerts are padding-only cases already validated in M3.26 targeted story pointers across M2-M4,12 getter windows/97bindings. This does not visually approve all886 literal story references/141presets. Storage preset32 caller remains unconfirmed.',planned_iterations=[1,2,3,4],completed_layout_iterations=4,remaining_base_layout_iterations=0)
 if x['id']=='TR-01-M2-C01':x.update(status='CANDIDATE_NOT_CONFIRMED_AFTER_M4',scope='Forced second page still exceeds the96px window. M4 found no validated native caller: at E0:11C2 opcode24 consumes17 as an argument, so11C3 is not an open-window instruction. At5ADB, opcode11 consumes0019, so5ADD is not a selection instruction. These injected mid-instruction entries are excluded diagnostics. No proof of unreachability; do not replace shared floor question F00:I053 or call this case PASS.',evidence='qa18/context_resolution.json')
 if x['id']=='TR-01-M3-C01':x.update(status='FIXED_PASS_SYNTHETIC_SCOPED_HF13',scope='Existing script E0:59B5 opens native one-line window1 and opcode28 at59BF readsG16:M064; old stream drops nonblank glyphs. Three input-paced pages now retain full rate and prompt. Inherited fo lot glyph sequence repaired to Slot. Native loop7B remains unchanged; scene reachability and real exchange transaction are not approved.',evidence='evidence/qa18_runs/final_slot_native')
for e in ed:
 if e['id']!='G16:M064':reg.append({'id':'M-18-'+e['id'].replace(':','-'),'status':'FIXED_PASS_SYNTHETIC_SCOPED_HF13','resource':e['id'],'scope':e['reason']})
reg.append({'id':'TR-01-L-G06-M073','status':'OPEN_INHERITED_TRANSLATION_DEFECT','resource':'G06:M073','scope':'The English sentence visibly ends will revert your level to, without a complement. M4 fixes pagination and word separation only. Compare complete Japanese explanation of the book sides and restore missing content in the separate bilingual revision; no linguistic PASS.'})
(R/'docs/issue_register.json').write_text(json.dumps(reg,indent=2)+'\n')
context={'slot':{'status':'FIXED_PASS_SYNTHETIC_SCOPED','script_entry':'E0:59B5','window':1,'caller':'E0:59BF opcode28 group10hex message40hex','native_line_limit':1,'observed_old_nonblank_drop_values':['00A4','00CE'],'new_pages':['1 Slot Point','100 Gil','Exchange Slot Points?'],'additional_glyph_repair':{'old':['00E6','035C','020B'],'new':['00D1','01A6','0278'],'origin':'Reuse S / lo / t-space already rendered in first line of same resource'},'native_loop':'E0:59C2 opcode7B ->59B5 preserved','natural_reachability':'NOT_VALIDATED','exchange_transaction':'NOT_VALIDATED'},'storage':{'status':'CANDIDATE_NOT_CONFIRMED','initializer':'ROM1860AF','consumer':'ROM188F2C','forced_index':53,'native_caller':'NOT_FOUND_IN_BOUNDED_INVESTIGATION','false_candidate_entry_points':['11C3: argument of opcode24 at11C2, confirmed by storage_full_native_v2 trace','5ADD: third byte of opcode11 at5ADB; injected interpretation is invalid','11BB: operand of preceding jump0F at11B9; diagnostic excluded'],'claim_of_unreachability':False,'rom_resource_modified':False,'next_action':'Recover a valid caller/state with actual storage list navigation before modifying F00:I053.'}}
(Q/'context_resolution.json').write_text(json.dumps(context,indent=2)+'\n')
gates={'scope':'HF13/M4 targeted layout, synthetic access authorized','DISCOVERED':'PASS_SCOPED','TRANSLATED':'NOT_GLOBALLY_VALIDATED','INTEGRATED':'PASS','RUNTIME_CONFIRMED':'PASS_SYNTHETIC_SCOPED','LINGUISTIC_APPROVED':'NOT_VALIDATED','TYPOGRAPHY_APPROVED':'PASS_SCOPED_INHERITED_FONT','LEGIBILITY_APPROVED':'PASS_SCOPED_14_NATIVE_READINGS','DESIGN_APPROVED':'PASS_SCOPED_EXISTING_WINDOWS','VISUAL_APPROVED':'PASS_SCOPED_NOT_GLOBAL','FUNCTIONAL_APPROVED':'PASS_SCOPED_TEXT_RENDER_AND_CONFIRMATION_ONLY','FINAL_APPROVED':False};(Q/'gates.json').write_text(json.dumps(gates,indent=2)+'\n')
fixes_es=[('G16:M064','Intercambio de puntos','Tres páginas con pausa; recuperación de letras recortadas y sustitución de «fo lot» por «Slot».'),('G00:M015','Disculpa','Pausa tras «Oh, sorry.»; la frase siguiente queda completa en dos líneas.'),('G06:M012','Camilla y la mazmorra','Tres páginas sin desplazamiento prematuro; espacio entre «Camilla’s» y «Dad».'),('G06:M073','Aviso del libro','«to» comparte línea con un separador; la advertencia final tiene página propia. Persiste una omisión de traducción.'),('G09:M191','Vacilación','Los puntos suspensivos se completan antes de la pausa y se limpia la ventana para la frase siguiente.')]
md='\n'.join(f'| {a} | {b} | {c} |'for a,b,c in fixes_es)
report=f'''# Chocobo — QA18 / Maquetación M4 de 4

HF13 TEST • 14 de octubre de 2026 • Japonés → inglés

La cuarta iteración está ejecutada: cinco recursos corregidos y siete pruebas finales con **PASS_SYNTHETIC_SCOPED**. Las cuatro iteraciones del plan han terminado. Esto cierra el lote M4 y los defectos demostrados de su alcance; **no concede aprobación visual exhaustiva a toda la ROM**.

| Recurso | Contexto | Corrección |
|---|---|---|
{md}

## Validación

- 7 sesiones finales, 7.500 cuadros nativos, 14 lecturas de capturas y 259 comprobaciones reproducibles.
- Cero glifos no vacíos perdidos en las siete sesiones. También pasan las regresiones de Cost65535 y nombre largo/Level65535.
- 147 bytes de contenido y 2 de checksum cambiados frente a HF12. Código, fuente, logo, tablas de punteros y recursos del getter idénticos.
- BPS aplicado mediante un decodificador independiente a la ROM japonesa limpia: igualdad de todos los bytes y SHA-256.
- 11 pruebas del proyecto aprobadas.790 comprobaciones QA17 repetidas sobre su HF12 histórico; sus29 sesiones conservan su alcance original y no se presentan como nuevas ejecuciones HF13.
- 30 sesiones archivadas:7 aprobadas y23 diagnósticas excluidas, incluidas compilaciones candidatas y entradas de script descartadas. Ninguna diagnóstica cuenta como PASS.

## Ventanas, saltos, recortes y variables

El censo completo de las tablas verificadas contiene3.488 referencias de diálogo (3.472 punteros),886 referencias con texto literal,2.421 no vacías compuestas sólo por controles,2.333 entradas del getter y141 presets de ventana (79 geometrías incluyendo modo). No hay cadenas sin terminador en esas tablas.

El barrido de ancho sólo conserva G01:M031,G06:M022 yG09:M063: sus excesos son relleno0000, comprobado en M3; no requieren recortar texto. El nuevo barrido de líneas explícitas entre pausas no deja candidatos verticales. Es un análisis estructural: no cubre por sí solo cualquier altura elegida por un consumidor ni toda combinación contextual de variables.

La matriz M2–M4 acredita26 punteros de diálogo probados como objetivo (28 referencias contando alias, sin atribuirles un caller independiente),12 ventanas del getter y97 enlaces ventana/familia/índice. Las9 referencias dinámicas comparten los7 punteros probados en M3; sus bytes y consumidores se conservan en HF13. Las14 páginas de créditos mantienen su comprobación M3. **Estas cifras no son un porcentaje de aprobación global**: falta revisión visual de los demás contextos reales.

## Pendientes concretos

1. **Preset32 / F00:I053:** el recorte aparece al forzar una segunda página. No se encontró una llamada nativa válida en esta investigación acotada. Dos aparentes llamadas resultaron ser argumentos de otras instrucciones. Se conserva como candidato no confirmado, sin afirmar que sea inalcanzable ni modificar la pregunta compartida sobre pisos.
2. **Cobertura visual global:** ampliar la matriz de consumidores y escenas antes de marcar TR-01-M como aprobado globalmente. Ejecutar cuatro iteraciones no prueba todas las886 referencias con texto ni los141 presets.
3. **Revisión lingüística separada:** G06:M073 termina «will revert your level to» sin complemento; conserva una omisión anterior. También siguen vigentes las observaciones lingüísticas de M3 (incluida la redacción del aviso de guardado). La maquetación de estas frases no certifica su traducción.

El acceso a los mensajes fue sintético: savestate más sustitución de selector o puntero de script; dos casos añaden valores extremos. El script de puntos se ejecuta con sus instrucciones y ventana originales, pero su entrada natural, la transacción económica y la persistencia del guardado no se validaron aquí. La rutina7B que repite ese script se conserva.

## Artefactos y reproducción

BPS acumulativo directo desde JP CRC32 **CCAA4853**. No se aplica sobre HF12 ni sobre una ROM inglesa. Fuentes completas reconstruidas y editables, evidencia histórica y nueva, planes Lua, estados compatibles, verificador y manifiesto incluidos. No se distribuye ROM ni BIOS.

```sh
python3 build.py /ruta/original-japonesa.ws --out /ruta/build-hf13
python3 qa18/verify_scope.py --japanese-rom /ruta/original-japonesa.ws --out /ruta/verificacion-qa18.json
python3 -m unittest discover -s tests
```

Para repetir una sesión con Mesen compatible, use qa18/run.py, qa18/driver.lua, el plan y la ruta de estado indicados en provenance.json de cada sesión, con LAYOUT_OBSERVER apuntando a qa18/layout_observer.lua. Las inyecciones operan en memoria del emulador y no son cambios de ROM.

SHA-256 JP: `{m['original']['sha256']}`

SHA-256 HF13: `{m['target']['sha256']}`

SHA-256 BPS: `{m['bps_sha256']}`

Checksum WonderSwan: **0903**. Estado de publicación: **TEST**, no RC ni FINAL_APPROVED.
'''
# Fix readability of generated prose spaces, not project data.
for a,b in [('contiene3.488','contiene 3.488'),('),886', '), 886'),(',2.421', ', 2.421'),(',2.333', ', 2.333'),('y141','y 141'),('acredita26','acredita 26'),('),12', '), 12'),('y97','y 97'),('Las9','Las 9'),('los7','los 7'),('Las14','Las 14'),('las886','las 886'),('los141','los 141'),('rutina7B','rutina 7B'),('proyecto aprobadas.790','proyecto aprobadas. 790'),('sus29','sus 29'),('archivadas:7','archivadas: 7'),('y23','y 23'),('relleno0000','relleno 0000'),('G01:M031,G06:M022 yG09:M063','G01:M031, G06:M022 y G09:M063')]:report=report.replace(a,b)
(R/'INFORME_ES.md').write_text(report);(R/'README.md').write_text('''# Chocobo English HF13 TEST — QA18/M4

Cuarta iteración de maquetación ejecutada. Cinco recursos corregidos; siete PASS sintéticos acotados. No existe aprobación visual o lingüística global. El caso preset32/F00:I053 sigue sin contexto confirmado.

Lea INFORME_ES.md, docs/issue_register.json y CONTEXTO_CONTINUACION.md. El paquete contiene fuentes acumulativas reconstruidas, BPS directo desde la ROM japonesa CRC32 CCAA4853 y evidencias; no contiene ROM ni BIOS.

```sh
python3 build.py /ruta/original-japonesa.ws --out /ruta/build-hf13
python3 qa18/verify_scope.py --japanese-rom /ruta/original-japonesa.ws --out /ruta/verificacion-qa18.json
python3 -m unittest discover -s tests
```

Aplicar patches/Chocobo_EN_v1.1_HF13_TEST_JP_CCAA4853.bps sólo a JP limpia. La carpeta patches/historical conserva los parches anteriores. Las verificaciones QA15/16/17 quedan ligadas a sus builds históricos, no al target actual.
''')
(R/'CONTEXTO_CONTINUACION.md').write_text(f'''# Estado vigente — HF13 TEST / QA18 M4

Juego: Chocobo no Fushigi na Dungeon (WonderSwan). Japonés a inglés. M4/4 ejecutada; cero iteraciones base restantes, sin convertirlo en aprobación global.

Target SHA256 {m['target']['sha256']}; BPS SHA256 {m['bps_sha256']}; JP CRC CCAA4853. Nunca tomar la base por fecha/nombre sin contrastar hash.

Nuevo: cinco recursos (qa18/edits.json),147 bytes de texto+2 de checksum. SlotPoints: entrada sintética al script E0:59B5, ventana1 de una línea, tres páginas con pausas; secuencia fo lot corregida con S/lo/t-space del mismo recurso. Cuatro mensajes adicionales con páginas/espaciado ajustados. Siete sesiones finales,7.500 cuadros,14 lecturas,259 comprobaciones. QA17 histórico revalidado790;11 unit tests PASS.

Pendientes reales: TR-01-M2-C01 preset32/F00:I053 (sin caller válido); revisión visual global de consumidores fuera de la matriz; TR-01-L lingüística. G06:M073 conserva una frase incompleta tras to: no aprobar semántica. M3 ya señaló G06:M099 yG16:M004. No repetir diagnóstico de cartucho físico ni convertir causas históricas desconocidas en bloqueos funcionales: los PASS sintéticos anteriores de equipamiento/Atla/ascensor/99→30/guardado siguen limitados a sus pruebas.

Fuentes y evidencia acumulativas: consultar qa18/coverage_summary.json,story_coverage.csv,context_resolution.json,gates.json,verification.json y docs/QA18_RUN_INDEX.json. Veintitrés diagnósticos excluidos; no usar pre_final ni candidate como evidencia de HF13 final. Los planes finales son los siete nombres final_* del índice.

Antes de continuar, recuperar este paquete completo y verificar manifest.json. No fabricar un nuevo BPS si no cambia la ROM. La cobertura de26 punteros de diálogo,12 ventanas/97bindings y9 referencias dinámicas es acotada: no afirmar que los886 diálogos literales y141presets fueron leídos en pantalla. Es posible seguir con otra etapa, pero no prometer una cantidad de iteraciones sin definir sus consumidores y casos.
''')
(Q/'completion.json').write_text(json.dumps({'completed_utc':now,'started_utc':json.loads((Q/'start.json').read_text())['start'],'iteration':'M4_OF_4','status':'EXECUTED_PASS_SYNTHETIC_SCOPED','output':'HF13_TEST','global_layout_approved':False,'global_linguistic_approved':False,'remaining_base_iterations':0},indent=2)+'\n')
# Self-contained HTML report; native screenshots are embedded, never generated.
img=base64.b64encode((Q/'final_contact.png').read_bytes()).decode();fixrows=''.join(f'<tr><td><code>{a}</code></td><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>'for a,b,c in fixes_es)
body=f'''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chocobo · QA18 M4 · HF13 TEST</title><style>body{{font:16px/1.6 system-ui,sans-serif;color:#20313a;background:#f4f2ea;margin:0}}main{{max-width:1120px;margin:auto;padding:36px 24px}}h1{{font-size:38px;line-height:1.1}}.tag{{color:#366c5f;font-weight:700;letter-spacing:.12em}}.card{{background:white;padding:22px;border-radius:12px;margin:22px 0}}table{{border-collapse:collapse;width:100%}}td,th{{padding:12px;text-align:left;border-bottom:1px solid #ddd;vertical-align:top}}code{{overflow-wrap:anywhere;font-size:.86em}}img{{width:100%;height:auto;image-rendering:pixelated}}.stats{{display:flex;gap:16px;flex-wrap:wrap}}.stats div{{flex:1;min-width:170px;background:#e1e9df;padding:18px;border-radius:8px}}strong.big{{display:block;font-size:30px}}footer{{font-size:13px;color:#53616a}}@media(max-width:700px){{table{{font-size:13px}}td,th{{padding:6px}}h1{{font-size:30px}}}}</style><main><p class="tag">CHOCOBO · WONDERSWAN · JAPÓN → INGLÉS</p><h1>Maquetación · iteración 4 de 4</h1><p>HF13 TEST · 14 octubre 2026</p><div class="card"><b>Iteración ejecutada: PASS sintético acotado.</b> Cinco recursos corregidos. El lote M4 está cerrado; la aprobación visual y lingüística global sigue pendiente.</div><div class="stats"><div><strong class="big">5</strong>recursos corregidos</div><div><strong class="big">7</strong>sesiones finales aprobadas</div><div><strong class="big">7.500</strong>cuadros nativos</div><div><strong class="big">259</strong>comprobaciones</div></div><section class="card"><h2>Correcciones entregadas</h2><table><thead><tr><th>Recurso</th><th>Contexto</th><th>Cambio</th></tr></thead><tbody>{fixrows}</tbody></table></section><section class="card"><h2>Capturas de la compilación final</h2><p>14 lecturas nativas. Se distinguen paginación, separación y valores máximos. La frase incompleta del libro permanece identificada para revisión lingüística.</p><img alt="Capturas nativas de las cinco correcciones y dos regresiones" src="data:image/png;base64,__NATIVE_CONTACT__"></section><section class="card"><h2>Qué está comprobado</h2><p>Cero glifos perdidos en las siete sesiones finales. BPS reaplicado a JP limpia con igualdad completa mediante decodificador independiente.147 bytes de contenido y2 de checksum frente a HF12; código, fuente, logo, punteros y getter conservados.11 pruebas del proyecto aprobadas.</p><p>El barrido de3.488 referencias no encuentra cadenas sin terminador ni páginas candidatas de más de dos líneas entre pausas. Las tres alertas de ancho restantes son relleno vacío verificado en M3.</p><p>La matriz M2–M4 registra26 punteros de diálogo objetivo,12 ventanas del getter y97 enlaces. Las9 referencias dinámicas comparten los7 punteros ya probados. Las29 sesiones M3 y sus14 páginas de créditos conservan su alcance histórico: se revalidaron790 comprobaciones sobre HF12.</p></section><section class="card"><h2>Qué continúa abierto</h2><ol><li><b>Almacén preset32 / F00:I053:</b> recorte bajo desplazamiento forzado, sin llamada nativa confirmada. Las aparentes llamadas investigadas incluían argumentos de otras instrucciones. Candidato, no defecto confirmado ni PASS.</li><li><b>Cobertura visual global:</b> no se han aprobado individualmente las886 referencias con texto ni los141 presets. El censo y las cuatro iteraciones no equivalen a revisión exhaustiva.</li><li><b>Traducción:</b> G06:M073 conserva «will revert your level to» sin complemento. Continúan las observaciones lingüísticas anteriores. No existe FINAL_APPROVED.</li></ol><p>Acceso por savestate e inyección de selector/puntero; dos regresiones usan datos extremos. No se valida entrada natural, transacción de puntos ni persistencia de guardado en M4.30 sesiones archivadas:7 finales y23 diagnósticas excluidas.</p></section><section class="card"><h2>Aplicación y trazabilidad</h2><p>Aplicar el BPS acumulativo a la ROM japonesa limpia CRC32 <b>CCAA4853</b>. No aplicarlo sobre HF12. El ZIP contiene fuentes editables acumulativas, planes, estados, capturas, manifiesto y verificadores; no incluye ROM ni BIOS.</p><p>HF13 SHA-256<br><code>{m['target']['sha256']}</code></p><p>BPS SHA-256<br><code>{m['bps_sha256']}</code></p><p>Checksum WonderSwan <b>0903</b> · Publicación <b>TEST</b></p></section><footer>Detalle técnico y pendientes en INFORME_ES.md, docs/issue_register.json y qa18/. Evidencia sintética autorizada por el usuario; aprobaciones limitadas al alcance documentado.</footer></main></html>'''
for a,b in [('independiente.147','independiente. 147'),('y2 ','y 2 '),('conservados.11','conservados. 11'),('de3.488','de 3.488'),('registra26','registra 26'),(',12 ', ', 12 '),('y97','y 97'),('Las9','Las 9'),('los7','los 7'),('Las29','Las 29'),('sus14','sus 14'),('revalidaron790','revalidaron 790'),('las886','las 886'),('los141','los 141'),('M4.30','M4. 30'),('archivadas:7','archivadas: 7'),('y23','y 23')]:body=body.replace(a,b)
body=body.replace('__NATIVE_CONTACT__',img)
reportpath=Path('delivery/Chocobo_QA18_M4_Informe.html');reportpath.write_text(body);shutil.copy2(reportpath,R/'QA18_M4_Informe.html');print('docs updated',now)
