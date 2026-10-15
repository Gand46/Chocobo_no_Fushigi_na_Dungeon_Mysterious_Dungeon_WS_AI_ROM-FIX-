from pathlib import Path
import json,hashlib,base64,html,shutil,datetime
R=Path('delivery/Chocobo_EN_v1.1_HF14_TEST_Fuentes_QA19_V1_20261014');Q=Path('qa19');m=json.loads((R/'manifest.json').read_text());v=json.loads((Q/'verification.json').read_text());review=json.loads((Q/'linguistic_review.json').read_text());plan=json.loads((Q/'five_validation_plan.json').read_text());vis=json.loads((Q/'visual_readings.json').read_text());alloc=json.loads((Q/'allocations.json').read_text());tr=json.loads((Q/'translations.json').read_text())
m['qa19'].update(status=v['status'],native_sessions=84,native_frames=v['native_frames'],visual_readings=101,linguistic_scoped_pass=82,context_pending=['G16:M073'],checks=v['checks'],portable_editable_rebuild='PASS_EXACT_ROM_AND_EDITS');m['visual_linguistic_validation']={'completed':1,'planned':5,'remaining':4,'global_approval':False,'completed_means':'Validation cycle executed; not every context approved'};m['corrected_resources']=None;m['corrected_resources_note']='Legacy counter retained separately; QA19 changes 36 references, including previously edited references, so it is not added to that counter.';m['intentional_near_pointer_edits']=41;m['generated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(R/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
summary=f'''# Chocobo English v1.1 HF14 TEST — QA19, validación 1/5

Validación 1/5 ejecutada con una reserva de contexto. 83 referencias revisadas, 36 corregidas, 82 con aprobación lingüística acotada y G16:M073 pendiente de su frase anfitriona. El estado global continúa TEST, sin aprobación visual/lingüística universal.

## Resultado comprobado

- 84 sesiones sintéticas nativas: 83 mensajes y el consumidor de Slot Points de una línea.
- {v['native_frames']} fotogramas; 101 lecturas visuales verificables; {v['checks']} comprobaciones automáticas de integridad y alcance.
- 11 pruebas del proyecto aprobadas. Los 259 controles históricos QA18 se verifican sobre HF13 preservado, no se presentan como pruebas nuevas sobre HF14.
- 0 glifos no vacíos descartados en las sesiones aprobadas; 1 descarte de relleno vacío.
- BPS reconstruido y aplicado con implementación independiente: igualdad exacta con HF14.
- Regenerador editable de las traducciones: produce la misma ROM y el mismo archivo de cambios.

## Correcciones relevantes

| Referencia | Corrección |
|---|---|
| G16:M004 | Sesión anterior terminada anormalmente; elimina la afirmación incorrecta de corrupción de datos. No identifica una causa de pérdida de guardado. |
| G16:M012–015, M020–024, M049–050 | Restaura fuente, grado de recuperación y matices de los efectos; distingue recuperación completa de aumento del máximo. |
| G16:M032, M047–048 | Diferencia desprender equipo maldito de quitar la maldición; explicita garras equipadas y equipo desprendido. No modifica la lógica del equipamiento. |
| G16:M037, M039, M043–045 | Cansancio/desfallecimiento, bolsa llena y movimiento/fuerza; elimina texto defectuoso. |
| G16:M051, M061, M064, M066 | Conserva descenso, corrige pregunta de canje, cantidad de puntos y límite de capacidad. |
| G16:M070–071 | Completa recomendación y consejos de Nakamura, incluidos los regresos frecuentes con Teleport Card. |
| G06:M073 | Explica portada/conservar nivel y contraportada/reiniciar nivel, sin inventar una advertencia irreversible. |
| G06:M099 | El intercambio comienza normalmente en el capítulo 3; no se refiere a objetos del capítulo 3. Conserva el resaltado. |
| Otras referencias del registro | Etiquetas, naturalidad, puntuación y separación de palabras. |

Las 36 referencias incluyen equivalencias y alias: no se presentan como 36 causas funcionales distintas. El registro completo está en qa19/linguistic_review.json, con imágenes japonesas originales en qa19/audit_00.png…audit_08.png y capturas nativas finales en evidence/qa19_runs/release2_*.

## Alcance y reservas

La revisión japonesa se realizó leyendo los glifos de la ROM original; el inglés final se leyó en capturas del motor nativo. Las capturas japonesas estáticas no se cuentan como sesiones de juego. Una sola revisión del asistente; no existe aprobación independiente de otra persona.

La selección de mensajes se fuerza desde un savestate. Para cinco referencias dinámicas se inyectó el nombre largo Double KnockTalon y, cuando corresponde, 65535. Esto demuestra el renderizado del caso probado, no todos los valores, consumidores o recorridos naturales. Slot Points también se ejecutó mediante su script y ventana de una línea. El resto de menús reales, en particular New Game/Unused/aviso de sesión, entra en V2.

G16:M073 mantiene «floors or so»: la referencia japonesa contiene un matiz temporal posterior. Falta localizar y leer la frase compuesta antes de decidir la traducción final. No obtiene PASS lingüístico completo.

El candidato heredado preset32/F00:I053 sigue sin consumidor válido confirmado; no se modifica basándose solo en la segunda página forzada. Las causas históricas de equipamiento, Atla y reset del guardado conservan sus límites anteriores; esta fase no reabre ni resuelve esas causas. Las pruebas sintéticas previas siguen documentadas. El incidente eléctrico del cartucho queda fuera de la ROM.

## Cinco validaciones

| Validación | Referencias literales | Alcance principal |
|---|---:|---|
| V1 | 83 | G16 + G06:M073/M099; ejecutada, con reserva G16:M073. |
| V2 | 248 | G00–G05 y consumidores reales de menús/guardado. |
| V3 | 207 | Resto de G06, G07, G08, G10, G11; léxico de objetos y variables. |
| V4 | 194 | G09; diálogos extensos y opciones. |
| V5 | 154 | G14; revisión transversal, gráficos/créditos y reservas. |

La partición suma las 886 referencias de historia con texto literal. El inventario contiene además 2421 referencias no vacías solo de control, 2333 entradas getter, 141 presets y 79 geometrías. Los gráficos y todos los consumidores getter no quedan aprobados por sumar estas cinco filas. El cierre global dependerá de los hallazgos y su evidencia, sin añadir automáticamente otra iteración.

## Reconstrucción

Aplicar Chocobo_EN_v1.1_HF14_TEST_JP_CCAA4853.bps directamente a una copia limpia japonesa CRC32 CCAA4853. No aplicar sobre una ROM inglesa o previamente parcheada.

```bash
python3 build.py '/ruta/Chocobo_JP.ws' --out '/ruta/salida_hf14'
python3 qa19/verify_scope.py --japanese-rom '/ruta/Chocobo_JP.ws' --out '/ruta/qa19_resultado.json'
python3 -m unittest discover -s tests -v
```

Para regenerar las frases editables:

```bash
python3 qa19/rebuild_translation_edits.py --japanese-rom '/ruta/Chocobo_JP.ws' --out '/ruta/generado_qa19'
```

qa19/translations.json contiene las páginas y líneas; text_codec.py contiene el mapa parcial de digrafos. El mapa no certifica automáticamente cualquier frase futura: cada nueva frase requiere lectura visual. El generador parte del HF13 preservado y produce candidate.ws, edits.json y allocations.json fuera del paquete. build.py es la reconstrucción acumulativa canónica basada en src/corrections.json. Para introducir cambios posteriores hay que integrar explícitamente los nuevos edits y volver a validar; editar translations.json por sí solo no altera el BPS.

## Integridad y conservación

Se usan {m['qa19']['unique_new_payloads']} bloques nuevos deduplicados, 1416 bytes del intervalo libre verificado 06:E000–06:FF00 y 36 redirecciones dentro del mismo banco. Cambian 1355 bytes respecto a HF13, incluidos los 2 del checksum. No cambia el tamaño de ROM ni el bloque de fuente; no se modifica código de juego. Los textos anteriores quedan preservados en sus ubicaciones. El analizador de inventario ahora usa el límite verificado de 256 entradas de G16, porque su primer texto ya no marca el final físico de la tabla después de reubicarlo.

- SHA-256 ROM japonesa: {m['original']['sha256']}
- SHA-256 ROM HF14: {m['target']['sha256']}
- CRC32 HF14: {m['target']['crc32']}; checksum WS: {m['target']['ws_checksum']}.
- SHA-256 BPS: {m['bps_sha256']}

Paquete acumulativo con fuentes editables reconstruidas, historial, planes, checkpoints, lecturas y evidencia. No contiene ROM comercial ni BIOS. Las fuentes no son el código original del juego. Solo release2_* se admite como evidencia final QA19; 416 sesiones anteriores son diagnósticas y quedan excluidas, incluso las que finalizaron con código 0. Algunas candidate_* mezclaron un archivo candidato modificado durante la tanda: sus hashes no sirven como prueba de versión. Se conservan sus registros y capturas para transparencia; los dumps y checkpoints completos se conservan para las 84 sesiones finales.
'''
(R/'README.md').write_text(summary);(R/'INFORME_ES.md').write_text(summary)
cont='''# Continuación — partir de HF14 / QA19 V1

Solicitado: aprobación visual/lingüística global, validación 1 de 5. V1 ejecutada; quedan V2–V5, no una supuesta aprobación global completa.

Prioridad siguiente: V2 (248 referencias de G00–G05), leer japonés/inglés y comprobar los consumidores reales de menú y guardado, incluidos G16:M000, M003 y M004. No volver a correr indiscriminadamente las pruebas de las causas históricas. Usar five_validation_plan.json para evitar duplicar cobertura.

G16:M073 necesita frase anfitriona; mantiene contexto pendiente. preset32/F00:I053 sigue sin consumidor válido, no confundir pruebas forzadas con bug natural. Los tres candidatos horizontales estáticos siguen siendo G01:M031, G06:M022 y G09:M063; conservan el análisis histórico y no son fallos nuevos demostrados.

Reanudar desde checkpoints en evidence/qa19_runs/release2_*; base general evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss, consumidor Slot evidence/qa16_runs/shop_enter/checkpoint.mss. Mesen y driver fijados en manifest/run.json. Una sola instancia de Mesen a la vez. No usar código de salida como PASS: exigir target_completed, FFFF exterior (estado sin bit40), páginas leídas e integridad de las variables. La pausa lleva bit80; en el automatismo comparar estado & 7F.

En text_codec.py, los glifos de una letra del lado derecho se reservan para prefijos sin digrafo; los finales usan el lado izquierdo. La fila y es irregular y «yo» fue sustituido en la fuente. No inferir automáticamente todo el mapa por aritmética. Las frases entregadas están verificadas visualmente.

La versión se mantiene TEST. PASS sintético autorizado por el usuario no prueba recorrido natural, segundo emulador o hardware. Mantener entregas de fuentes acumulativas completas + BPS directo JP + evidencia, sin ROM. Conservar límite de emergencia de 40 minutos por turno; guardar checkpoint antes de cortar.
''';(R/'CONTEXTO_CONTINUACION.md').write_text(cont)
# Self-contained report with exact final images; no substitutions inside base64.
esc=html.escape
def im(p,alt):return '<img alt="'+esc(alt)+'" src="data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()+'">'
css='body{font:16px system-ui,sans-serif;background:#eef2f0;color:#192a24;margin:auto;max-width:1120px;padding:32px;line-height:1.5}h1{font-size:36px;line-height:1.15}h2{margin-top:32px}table{border-collapse:collapse;width:100%;background:white}td,th{padding:10px;text-align:left;border-bottom:1px solid #ccd7d1}code{overflow-wrap:anywhere}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(224px,1fr));gap:16px}.card,details{background:white;border-radius:10px;padding:16px;margin:12px 0}img{max-width:100%;height:auto;image-rendering:pixelated}summary{cursor:pointer;font-weight:650}.note{border-left:5px solid #c48524;padding:12px;background:#fff3d9}.tag{color:#236346;font-weight:700}small{color:#53685e}'
s='<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chocobo HF14 · Validación 1/5</title><style>'+css+'</style><body><small>CHOCOBO · WONDER SWAN · QA19 / HF14 TEST</small><h1>Validación visual y lingüística 1 de 5</h1><p class="tag">Ciclo ejecutado · PASS sintético acotado · aprobación global pendiente</p><div class="grid">'+''.join('<div class="card"><h2>'+str(n)+'</h2>'+label+'</div>'for n,label in [(83,'referencias revisadas'),(36,'referencias corregidas'),(82,'aprobaciones lingüísticas acotadas'),(84,'sesiones sintéticas aprobadas')])+'</div><p class="note">Una reserva: G16:M073 («floors or so») necesita su frase anfitriona. Los menús reales restantes se comprueban en V2; la selección sintética de un texto no certifica todos sus consumidores.</p><p>101 lecturas visuales, 20 666 fotogramas, 1353 controles, 11 pruebas del proyecto y BPS independiente idéntico. Una sola revisión del asistente; no es aprobación humana independiente.</p><h2>Correcciones en pantalla</h2><div class="grid">'
for id,cap in [('G16_M004','Aviso fiel de sesión anterior'),('G16_M032','Equipo maldito desprendido'),('G16_M066','Capacidad de puntos'),('G06_M073','Portada y contraportada'),('G16_M071','Consejos completos'),('G06_M099','Intercambio desde capítulo 3')]:
 r=Q/'runs'/('release2_'+id);s+='<div class="card"><strong>'+cap+'</strong>'+''.join(im(p,cap)for p in sorted(r.glob('page_*.png')))+'</div>'
s+='</div><h2>Ventana de una línea</h2><div class="grid">'+''.join('<div class="card">'+im(Q/'runs/release2_slot_native'/n,n)+'</div>'for n in ['f00150.png','f00420.png','f00780.png'])+'</div><h2>Registro de las 83 referencias</h2><p>Desplegar cada referencia para ver significado revisado y páginas finales. Las capturas estáticas japonesas originales figuran al final.</p>'
for row in review:
 rid=row['id'];rname='release2_'+rid.replace(':','_');s+='<details><summary>'+esc(rid+' · '+row['action']+' · '+row['linguistic_status'])+'</summary><p>'+esc(row['source_meaning_es'])+'</p>'
 if rid in tr:s+='<p><strong>Inglés:</strong> '+esc(' / '.join(' | '.join(x)for x in tr[rid]))+'</p>'
 s+='<div class="grid">'+''.join('<div>'+im(Q/'runs'/rname/x['image'],rid)+'</div>'for x in vis if x['run']==rname)+'</div></details>'
s+='<h2>Plan de las cinco validaciones</h2><table><tr><th>Validación</th><th>Referencias de historia</th><th>Estado</th></tr>'+''.join('<tr><td>'+k+'</td><td>'+str(n)+'</td><td>'+('Ejecutada con una reserva'if k=='V1'else'Pendiente')+'</td></tr>'for k,n in plan['counts'].items())+'</table><p>886 referencias literales repartidas sin duplicados. Getters, gráficos y consumidores reales se evalúan además; esta suma no constituye una aprobación global.</p><details><summary>Comparación original japonesa / HF13 anterior</summary><p>Imágenes estáticas leídas, conservadas para comprobar los hallazgos; no son capturas runtime del parche final.</p>'+''.join(im(p,p.name)for p in sorted(Q.glob('audit_*.png')))+'</details><h2>Notas técnicas y límites</h2><p>1355 bytes cambiados respecto a HF13. 36 redirecciones dentro del mismo banco y 1416 bytes de mensajes nuevos deduplicados. Fuente nativa y código de juego intactos. Se preservan fixes previos; no se vuelve a certificar su causa histórica en esta fase.</p><p>Los recorridos se acceden mediante savestate e inyección documentada. No se certifican recorrido natural, hardware o segundo emulador. 416 sesiones diagnósticas quedan excluidas del resultado final; solo release2_* aporta evidencia final.</p><p>Aplicar el BPS acumulativo directamente a la ROM japonesa limpia CRC32 CCAA4853.</p><p>SHA-256 HF14: <code>'+m['target']['sha256']+'</code></p><p>SHA-256 BPS: <code>'+m['bps_sha256']+'</code></p><p>Las fuentes completas incluyen README, registro bilingüe, plan V2–V5, regenerador editable, comprobador de alcance, historial y checkpoints. No se distribuye la ROM.</p></body></html>'
report=Path('delivery/Chocobo_QA19_V1_Informe.html');report.write_text(s);(R/'QA19_V1_Informe.html').write_text(s)
for n in ['write_docs.py','unit_result.json','historical_qa18_check.json']:shutil.copy2(Q/n,R/'qa19'/n)
print('report bytes',report.stat().st_size,'target',m['target'])
