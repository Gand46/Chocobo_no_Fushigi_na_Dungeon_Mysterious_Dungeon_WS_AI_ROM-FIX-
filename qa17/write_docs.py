from pathlib import Path
import json,hashlib,csv,shutil,base64,html
Q=Path('qa17');ROOT=Path('delivery/Chocobo_EN_v1.1_HF12_TEST_Fuentes_QA17_M3_20261014');R=Q/'runs';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();vis=[]
def reading(run,img,text,scope='PASS_VISUAL_SCOPED'):
 p=R/run/img;vis.append(dict(run=run,image=img,sha256=sha(p),observed=text,status=scope,method='Native pixels read before consulting expected strings; same model reviewer, no independent reviewer.'))
readings={
'G01_M039':[(420,'Without an edge.. / Smells that way.')],
'G03_M012':[(420,'Wah! Thanks, brother!')],
'G04_M031':[(420,"I worry for / Camilla’s Dad,"),(690,'but also the dungeon...')],
'G04_M034':[(420,'1000 Gil, OK? / 500 Gil, OK?')],
'G04_M048':[(420,'What is it? / Another Teleport Box?')],
'G06_M099':[(420,'Debug mode active.'),(690,'Only Chapter 3 items / onward can exchange! — fits; pre-existing awkward grammar retained, global linguistic approval not granted.')],
'G08_M020':[(420,'Chip and Mill / had babies!'),(690,'It was triplets!')],
'G16_M004':[(420,'! WARNING!'),(690,'Last play data / was corrupted. — visible wording only; does not establish actual save corruption or its cause.')],
'G16_M070':[(420,'Message from director / Koichi Nakamura!'),(690,'If you enjoy this game, / I recommend'),(930,'Shiren the Wanderer!')],
'G01_M031':[(420,'Applying oil would help.')],
'G06_M022':[(420,'That moogle is so lively!')],
'G09_M063':[(420,'Go out if it gets rough!')],
'G01_M040':[(420,'Well, why not / check it?')],
'G05_M002':[(420,'Using it, you can easily / go from 2F to 1F!')]}
for n,rs in readings.items():
 for f,t in rs:reading('final_'+n,f'f{f:05d}.png',t)
for mode,num,item in [('min','0','Ore'),('max','65535','Double KnockTalon')]:
 texts={'G00_M252':f'{num} Level','G00_M253':f'Cost {num} Gil','G00_M254':f'{item} Items','G00_M255':f'Name {item}','G16_M011':f'{item} / was covered in oil.','G16_M034':f'{item} / Level {num}!','G16_M253':f'{item} stolen.'}
 for n,t in texts.items():reading('final_dyn_'+n+'_'+mode,'f00420.png',t)
ct=['Chocobo for WS','SQUARE STAFF','Shinji Hashimoto','Kazuhiko Yoshioka / Toshiyuki Itahana','Katsuyoshi Kawahara / Masashi Kouda','Kazuhiko Aoki','Masashi Hamauzu','Izumi Tsukushi / Ichiro Hazama','BANDAI STAFF','PRODUCER / Takeo Isogai','SPECIAL THANKS / Yusuke Sasaki','Nobuyuki Tanaka / Toshihiro Suzuki / Hiromi Horiuchi','Hiroshi Shimada / Hirotaka Watanabe / Tsuyoshi Satou','Takahiro Sasanoi / Machiko Tsukui']
for p,t in zip(sorted((R/'final_credits').glob('credits_*.png')),ct):reading('final_credits',p.name,t+' — complete visible text, no clipping observed; name spelling not independently checked.')
reading('final_credits','f07200.png','Village scene after complete credit sequence; continued native execution.')
(Q/'visual_readings.json').write_text(json.dumps(vis,indent=2,ensure_ascii=False)+'\n');shutil.copy2(Q/'visual_readings.json',ROOT/'qa17/visual_readings.json');shutil.copy2(Q/'verify_scope.py',ROOT/'qa17/verify_scope.py')
# Reconcile the issue registry without changing historical functional verdicts.
p=ROOT/'docs/issue_register.json';issues=json.loads(p.read_text())
for x in issues:
 if x['id']=='TR-01-M':x.update(status='OPEN_M3_EXECUTED_SCOPED_PASSES',scope='M3/HF12: 11 unique resources corrected (13 references),29 scoped synthetic passes. Of13 inherited story alerts,9 fixed,3 padding-only,1 composite consumer unresolved.14 variable cases and14 credit pages reviewed. M4 must resolve remaining consumers and reconcile coverage.',completed_layout_iterations=3,remaining_base_layout_iterations=1)
 if x['id']=='M-15-02':x.update(status='FIXED_PASS_SYNTHETIC_HF12',scope='G03:M012: Japanese thanks-to-brother meaning checked; remove erroneous ff suffix and complete with exclamation. Native output and confirmation pass.',evidence='evidence/qa17_runs/final_G03_M012')
 if x['id']=='TR-01-L':x['qa17_note']='G03:M012 suffix resolved; global bilingual review remains open. G06:M099 awkward legacy wording and G16:M004 corruption wording require separate linguistic/contextual review.'
issues += [dict(id='TR-01-M3-C01',status='CANDIDATE_CONTEXT_NOT_VALIDATED',resource='G16:M064',scope='41-cell slot-point/cost composite. Forced common-story renderer drops two nonblank glyphs, but real production consumer/caller remains unproven. Do not impose 13-column reflow on this composite.',evidence='evidence/qa17_runs/final_G16_M064')]
for e in json.loads((Q/'edits.json').read_text()):issues.append(dict(id='M-17-'+e['id'].replace(':','-'),status='FIXED_PASS_SYNTHETIC_SCOPED_HF12',resource=e['id'],scope=e['reason']))
p.write_text(json.dumps(issues,indent=2,ensure_ascii=False)+'\n')
rows=[]
fixed=set(readings)-{'G01_M031','G06_M022','G09_M063','G01_M040','G05_M002'}
for n in sorted(fixed):rows.append(dict(resource=n.replace('_',':'),status='FIXED_PASS_SYNTHETIC',evidence='final_'+n))
for n in ['G01_M031','G06_M022','G09_M063']:rows.append(dict(resource=n.replace('_',':'),status='PASS_SYNTHETIC_PADDING_ONLY_NO_VISIBLE_LOSS',evidence='final_'+n))
rows.append(dict(resource='G16:M064',status='NOT_VALIDATED_ACTUAL_COMPOSITE_CONSUMER',evidence='final_G16_M064'))
with (ROOT/'qa17/alert_resolution.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
gates={'DISCOVERED':'PASS','TRANSLATED':'PASS_SCOPED_EDITS_ONLY','INTEGRATED':'PASS','RUNTIME_CONFIRMED':'PASS_SYNTHETIC_SCOPED','LINGUISTIC_APPROVED':'NOT_VALIDATED_GLOBAL','TYPOGRAPHY_APPROVED':'PASS_SCOPED','LEGIBILITY_APPROVED':'PASS_SCOPED','DESIGN_APPROVED':'N/A_NO_NEW_VISUAL_DESIGN','VISUAL_APPROVED':'PASS_SCOPED','FUNCTIONAL_APPROVED':'PASS_SCOPED_INPUT_AND_RETURN','FINAL_APPROVED':False}
(ROOT/'docs/QA17_GATES.json').write_text(json.dumps(gates,indent=2)+'\n')
summary='''# QA17 / Maquetación global, iteración 3 de 4

HF12 TEST integra 11 correcciones de recursos únicos (13 referencias, porque G16:M034/035/036 comparten puntero). Son 203 bytes de contenido y 2 de checksum respecto de HF11. El parche es acumulativo y se aplica directamente a la ROM japonesa CRC32 CCAA4853. No se modificaron el código ejecutable, los punteros, la fuente ni el logo.

29 pruebas sintéticas aprobadas en la compilación final, con 0 glifos visibles descartados. Se archivan 78 ejecuciones en total: las pruebas de diagnóstico, compilaciones intermedias y un timeout de instrumentación están excluidos del PASS. Ninguno se presenta como recorrido natural.

De las 13 alertas heredadas: 9 corregidas, 3 sólo afectan relleno vacío y 1 sigue pendiente de consumidor real (G16:M064). También se corrigió la unión «Price65535» mediante «Cost 65535» y la unión del nombre del objeto con «Level», ahora en una línea aparte. Hay 14 casos de variables para 7 punteros únicos / 9 referencias y 14 pantallas de créditos identificadas C5..D2. Las confirmaciones finalizan los mensajes; los créditos regresan al pueblo.

Las variables usan 0 y 65535 como extremos del formateador de 16 bits; 65535 no se declara un nivel alcanzable. Los nombres probados son Ore (1 celda) y Double KnockTalon (9 celdas), máximo ordinario de esta familia. Se excluye el recurso compuesto de moneda I012. FFF8 selector1 usa un buffer preparado con palabras exactas de la ROM: valida el consumidor, no la preparación natural del buffer. M035/M036 se cubren estructuralmente por identidad del puntero M034, no por rutas naturales separadas.

Los tres casos de relleno más tres variantes dinámicas máximas consumen un espacio invisible al avanzar: 6 eventos, 0 pérdidas visibles. No se ocultan ni se contabilizan como fallos corregidos. El recurso compuesto G16:M064 sólo falla al forzarlo por un consumidor que puede no corresponderle, y por eso queda NOT_VALIDATED.

## Cambios

- G01:M039: recuperar el terminador antes de G01:M040; conservar pausa y reducir un punto de la elipsis. M040 se comprobó por separado y sus bytes permanecen intactos.
- G03:M012: eliminar el sufijo «ff» residual, cotejando el agradecimiento al hermano con el japonés.
- G04:M031: saltos y pausa entre el nombre coloreado y la frase de la mazmorra.
- G04:M034: ambas confirmaciones de precio completas, 1000/500 Gil; eliminar residuos.
- G04:M048: «What is it? / Another Teleport Box?» completo y sin residuos.
- G06:M099: mover el salto; conservar todos los glifos, color y espera. La gramática heredada sigue pendiente de revisión lingüística.
- G08:M020: nombres / nacimiento / trillizos completos, con pausa y limpieza entre páginas.
- G16:M004: aviso y texto de guardado completos en dos páginas. Hacer legible el aviso no demuestra corrupción ni causa del reset; su formulación inglesa requiere revisión lingüística frente al japonés.
- G16:M070: tres páginas legibles, sin cortar «recommend» ni «Wanderer».
- G00:M253: separar etiqueta y cifra con «Cost».
- G16:M034/035/036: nombre en primera línea; «Level» y cifra en segunda.

## Pendientes concretos para M4

1. G16:M064: identificar el consumidor/caller del texto compuesto de puntos y precio antes de intervenirlo.
2. TR-01-M2-C01: identificar el caller válido de preset32 y su segunda página. La pregunta compartida F00:I053 no se cambia sin resolver sus usos.
3. Reconciliar la cobertura por contextos reales y la regresión de maquetación. El censo tiene 3488 referencias narrativas y 2333 entradas getter, pero esos totales no equivalen a aprobaciones visuales. No se ha completado el denominador de todos los contextos.

Queda 1 iteración base de maquetación; no es garantía de aprobación global. La revisión lingüística global es un bloque separado y permanece abierta. Se conservan los PASS sintéticos funcionales previos; las causas históricas exactas de equipamiento, Atla y reset de guardado no fueron reproducidas nuevamente en M3. El incidente eléctrico físico sigue fuera del alcance de la ROM.

Estado: TEST, no RC ni FINAL_APPROVED. Segundo emulador y hardware no validados. Los detalles verificables están en docs/QA17_VALIDATION.json, docs/QA17_RUN_INDEX.json, qa17/visual_readings.json y qa17/alert_resolution.csv.
'''
(ROOT/'INFORME_ES.md').write_text(summary);(ROOT/'docs/QA17_RESULTADO.md').write_text(summary)
readme='''# Chocobo English HF12 TEST — QA17 / M3

Fuentes acumulativas editables y parche BPS directo desde la ROM japonesa de WonderSwan. Sin ROM completa, BIOS ni emulador.

Base: 2 MiB, CRC32 CCAA4853, SHA-256 `38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728`.
Salida HF12: SHA-256 `ffb5561da6e9f15df0bdd3e028fe78b19f05a79916f88cc5503ea25216bfe3d1`, CRC32 `58CEAE7E`, checksum `FA41`.

Aplicar `patches/Chocobo_EN_v1.1_HF12_TEST_JP_CCAA4853.bps` a una copia limpia de la ROM japonesa, no a HF11. La aplicación del parche debe verificar la base.

Reconstruir y comprobar con Python 3 desde esta carpeta:

```sh
python3 build.py "/ruta/original-japonesa.ws" --out "/ruta/salida-nueva"
python3 qa17/verify_scope.py --japanese-rom "/ruta/original-japonesa.ws" --out "/ruta/validacion-qa17.json"
```

`src/legacy_translation_ranges.json` reconstruye la traducción previa; `src/corrections.json` contiene todas las correcciones acumulativas con precondiciones. `build.py` comprueba hashes, límites, checksum y BPS. No se requiere ejecutar los scripts de experimentación con rutas del entorno original para reconstruir la versión.

Los verificadores QA15 y QA16 se fijaron explícitamente al BPS histórico HF11 conservado. Sus comprobaciones archivadas pasan y no se presentan como nuevas sesiones HF12. La validación actual es QA17. `evidence/qa17_runs/*/provenance.json` conserva la ruta y hash del checkpoint, la inyección y el observador. `qa17/run.py` requiere un Mesen compatible con Lua; el binario usado está identificado por SHA en manifest.json.

29 PASS_SYNTHETIC acotados. 11 recursos únicos corregidos, 14 casos de variables y 14 pantallas de créditos. M3 de 4 ejecutada; maquetación y fidelidad lingüística global siguen abiertas. Leer INFORME_ES.md y CONTEXTO_CONTINUACION.md antes de continuar.
''';(ROOT/'README.md').write_text(readme)
context='''# Continuar desde HF12 TEST / QA17 M3

M3 de 4 ejecutada. Siguiente: M4 de maquetación; 1 iteración base restante, no garantía de cierre global. Autoridad: manifest.json, docs/QA17_VALIDATION.json, QA17_RUN_INDEX.json, issue_register.json y qa17/visual_readings.json. No retomar HF11 como base vigente.

HF12 SHA256 ffb5561da6e9f15df0bdd3e028fe78b19f05a79916f88cc5503ea25216bfe3d1. BPS directo JP CCAA4853 SHA256 fa8a91019a1994a060c43c23827ae624b3bfe82c7164390f1e12b1ae9d92516a. 205 bytes frente a HF11:203 texto,2 checksum.11 recursos únicos/13 referencias. Sin cambios de código, fuente, logo, tablas de punteros, guardado o combate.

Resultados M3:29 PASS sintéticos,78 ejecuciones archivadas (49 diagnósticas excluidas, incluido un timeout por observación amplia).9 de13 alertas narrativas reparadas;3 son relleno sin pérdida visible;G16:M064 queda pendiente de consumidor real.14 casos dinámicos para7 punteros/9 referencias.14 pantallas de créditos C5..D2: consumidor CPU503C2 y secuenciador157830..15795C, tabla de descriptores15043C+id*6, bancoE6. Los14 tilemaps comprimidos son idénticos al japonés. La fuente de créditos no se declara idéntica al JP; sí se conserva frente a HF11.

Correcciones, preimágenes y rangos en qa17/edits.json y src/corrections.json. G01:M039 invadía G01:M040 por falta deFFFF; se restaura el límite y se pruebaM040 por separado. G04:M031 yG16:M070 crecen únicamente dentro de sus slots originales, comprobados contra el siguiente puntero de todas las tablas narrativas. Las otras ediciones son iguales o más cortas. Los tails no referenciados pueden conservar bytes antiguos; no recontarlos como texto mostrado.

Dinámicos: FFF4 selector0 y0100 usan word67C6; la selección depende del nibble bajo, no del byte alto. FFF8 selector0 copia F03:[64CB] desde16E7F0 a6440. Selector1 no prepara el buffer: G00:M255 se ensaya con fixture de palabras exactas deF03, no se acredita su preparación natural. Valores0/65535 prueban formateador16bit, no niveles alcanzables. I217/I136 son nombres de1/9 celdas. I012 de13celdas es moneda compuesta y se excluye del máximo de nombre ordinario. M034/035/036 comparten06D028. Tres máximos descartan sólo0000 de relleno, igual que las3 alertas estáticas sin daño visible.

Acceso de diálogos: checkpoint evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss, hash6c5bcdf413ba34adf9bcb4bf3268469e1b2b6da48f623d4c270b210bc83ad92f. Hook único CPU50E77 antes de la selección; cambiar648F/648E. No alterar texto/píxeles/geometría. Motor común13celdas16px, lectura15113B/151158; encol13 consume y descarta el próximo glifo y avanza. FFF2pausa; FFFDlimpia; FFFE salto. Es acceso sintético autorizado, no ruta natural.

Pendientes M4: (1) G16:M064, compuesto41celdas slot-point/precio: la inyección en motor común descarta2glifos pero el consumidor real no está demostrado; no reflujo ciego. (2) TR-01-M2-C01: preset32 init1860AF / row188F2C / F00:I053; caller yscroll5 pendientes, no sustituir porStore6 sin resolver usos. (3) reconciliar contextos y regresión global;141presets/79geometrías no son un denominador de rutas reales. Mantener TR-01-L separado: gramáticaG06:M099 y sentido del avisoG16:M004 aún requieren revisión. Hacer visible “was corrupted” no prueba corrupción o causa del reset.

QA13funcional yQA14logo heredados por bytes no afectados; no repetir barridos255objetos/96propiedades ni guardado/Atla/equipamiento sin riesgo nuevo. QA15/16verificadores ejecutados contraHF11histórico explícito. Las causas históricas no se cierran conM3. Las fuentes y estados siguen siendo TEST. No se incluyeROM/BIOS/emulador.
''';(ROOT/'CONTEXTO_CONTINUACION.md').write_text(context)
p=ROOT/'CHANGELOG.md';p.write_text('# QA17 / HF12 — Maquetación M3 (2026-10-14)\n\n11 recursos únicos corregidos;29 PASS sintéticos;14 pantallas de créditos.205bytes frente aHF11. M4 y revisión lingüística global pendientes. Ver INFORME_ES.md.\n\n'+p.read_text())
# Keep final contacts within the reproducible source package.
for n in ['final_corrected_contact.png','final_dynamic_contact.png','credits_final_contact.png','regression_contact.png']:shutil.copy2(Q/n,ROOT/'qa17'/n)
print('visual observations',len(vis))
