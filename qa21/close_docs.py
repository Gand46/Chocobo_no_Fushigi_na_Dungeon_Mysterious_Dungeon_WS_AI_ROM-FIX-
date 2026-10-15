from pathlib import Path
from datetime import datetime,timezone
import json,shutil,hashlib
R=Path('work/Chocobo_QA20_V2');Q=Path('qa21');v=json.loads((Q/'verification.json').read_text());s=json.loads((Q/'supplemental_verification.json').read_text());m=json.loads((R/'manifest.json').read_text());now=datetime.now(timezone.utc).isoformat();m['qa21']=v|{'supplemental':s,'unit_tests_passed':11,'portable_editable_rebuild':'PASS_EXACT_ROM_AND_EDITS','second_independent_reviewer':False,'completed_utc':now};m['generated_utc']=now;m['date']='2026-10-15';m['date_timezone']='Etc/UTC';(R/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
text=f'''# Chocobo English v1.1 HF16 TEST — QA21, validación 3/5

V3 ejecutada con reservas: **207 referencias revisadas, 64 diálogos corregidos, 205 aprobaciones sintéticas acotadas y dos reservas**. También se corrigieron dos etiquetas de propiedades de equipo. La aprobación visual/lingüística global sigue abierta: quedan V4, V5 y los contextos pendientes.

## Resultado comprobado

- 207 selecciones sobre la ROM final; {v['story_terminators_reached']} alcanzan el terminador, {v['native_frames']} cuadros y {v['visual_readings']} capturas registradas. Ningún glifo no vacío descartado en las 205 referencias aprobadas.
- Complemento: cuatro recorridos de inventario/estado y seis configuraciones de equipo fusionado, en cinco sesiones finales y cinco japonesas de comparación. {s['final_frames']} cuadros finales; {s['native_readings']} imágenes de comparación leídas. Cantidades 1/99, equipo ±99, dinero de ocho cifras, nombres sin identificar y ocho propiedades.
- {v['checks']} controles del lote y {s['checks']} del complemento; 11 pruebas del proyecto aprobadas. Builder acumulativo, regenerador editable y aplicación BPS independiente producen exactamente la misma ROM.
- 64 bloques nuevos y 64 punteros en el banco 06: 06:E588–06:F708, final exclusivo, 4480 bytes. Dos propiedades se corrigen en su espacio original, sin mover sus punteros. {m['changed_bytes_vs_hf15']} bytes distintos frente a HF15, incluido checksum.
- Motor, fuente compartida, título, lógica de guardado y tamaño de ROM conservados. Los getters cambian únicamente en F06:I019 y F06:I022.

## Correcciones

Se recuperan sujetos, cantidades, causas, despedidas e instrucciones omitidas. Se repara una frase ilegible sobre el crecimiento del pueblo y la repetición de Item File. La explicación del cristal vuelve a incluir su división y expansión. Se mejora la gramática, la posesión de los personajes y el tratamiento Professor en este grupo. Las propiedades ahora dicen Strong vs undead y Strong vs poison foes: eficacia contra tipos de enemigos, no resistencia al estado veneno.

Detalle: qa21/translations.json (64 diálogos), qa21/getter_translations.json (dos propiedades), qa21/linguistic_review.json y QA21_V3_Informe.html. La tipografía conserva sus medias celdas, glifos y resaltados nativos.

## Reservas y límites

G06:M100 requiere su consumidor de depuración. G11:M011 es el fragmento de un número de plantas: falta la ventana compuesta y su cantidad real. Tener una captura aislada no los aprueba. La muestra de inventario no equivale a revisar todos los objetos ni los 2333 getters.

Se mantienen las seis reservas de V2: G00:M252–255 y G04:M033–034. También G16:M073, preset32/F00:I053 y los consumidores propios G16:M000/M003/M004. No se atribuyen etiquetas de G16 a menús con texto parecido. No se acredita recorrido natural completo, hardware, segundo emulador o segundo revisor.

Los 3787 controles históricos de QA20 se repitieron sobre HF15 preservado; no son nuevas sesiones V2 sobre HF16. Las matrices de guardado y las causas históricas no reproducidas mantienen sus límites anteriores.

| Validación | Referencias | Estado |
|---|---:|---|
| V1 | 83 | 82 aprobaciones acotadas; una reserva. |
| V2 | 248 | 242 aprobaciones acotadas; seis reservas. |
| V3 | 207 | 205 aprobaciones acotadas; dos reservas; complemento de inventario. |
| V4 | 194 | Siguiente: G09, diálogos extensos y opciones. |
| V5 | 154 | G14 y revisión transversal, gráficos, créditos, terminología y reservas. |

No se añade automáticamente una sexta fase ni se declara aprobación universal por contar las 886 referencias literales.

## Aplicación y reconstrucción

Aplicar **Chocobo_EN_v1.1_HF16_TEST_JP_CCAA4853.bps** directamente sobre una ROM japonesa limpia, CRC32 **CCAA4853**. Es acumulativo; no se aplica sobre una ROM inglesa ni sobre HF15.

```bash
python3 build.py '/ruta/Chocobo_JP.ws' --out '/ruta/salida_hf16'
python3 qa21/rebuild_translation_edits.py --japanese-rom '/ruta/Chocobo_JP.ws' --out '/ruta/frases_qa21'
python3 qa21/verify_scope.py --japanese-rom '/ruta/Chocobo_JP.ws' --out '/ruta/verificacion_qa21.json'
python3 -m unittest discover -s tests -v
```

El regenerador recompone HF15 con las recetas incorporadas y el snapshot docs/history/qa20/corrections.json; después genera los textos y propiedades QA21. No necesita recuperar un ZIP anterior. Cambiar un JSON de traducción requiere reintegrar los edits y repetir la validación; no modifica automáticamente el BPS.

Son fuentes acumulativas editables reconstruidas, no el código fuente original del juego. Se conserva el historial, la evidencia y los checkpoints. No se incluye ROM comercial, BIOS ni emulador. HF15 queda intacto en patches/historical. Los informes de dos reconstrucciones desde extracciones nuevas están en .continuity/reports.

## Integridad

- JP SHA-256: {m['original']['sha256']}
- HF16 SHA-256: {m['target']['sha256']}
- HF16 CRC32: {m['target']['crc32']}; checksum WS: {m['target']['ws_checksum']}.
- BPS SHA-256: {m['bps_sha256']}
'''
(R/'README.md').write_text(text);(R/'INFORME_ES.md').write_text(text)
context=f'''# Continuación — HF16 / QA21 V3

Objetivo: aprobación visual/lingüística global en cinco validaciones. V3 ejecutada con 207 referencias,64 diálogos corregidos,205 PASS sintéticos acotados y dos reservas. Dos propiedades getter corregidas. Global abierto; siguiente V4:194 referencias de G09 de qa19/five_validation_plan.json. V5:154 de G14 más transversal/reservas. No añadir otra fase automáticamente.

Autoridad de partida HF15/QA20: ZIP82f9bbe4007a56c93f223b84a39acc163f223d72bc1c04d61a9a4c8a23d9913b; snapshot481fcb1bcd729cc7c4d5908e10aa3e9055c65dcae393487104aa8af3e6ca115b. Se verificaron65488 archivos antes de editar. Partir ahora de este paquete HF16 y comprobar .continuity antes de nuevos cambios.

ROM final {m['target']['sha256']}; CRC{m['target']['crc32']}; checksum{m['target']['ws_checksum']}. Builder canónico src/corrections.json; regenerador qa21/rebuild_translation_edits.py parte del snapshot HF15 incorporado. QA20 histórico se fija a su BPS y recetas originales.

Evidencia final del lote: evidence/qa21_runs/verified_G*. Prefijos baseline_,final_,pregetter_,release_,rejected_,repair_ son diagnósticos o fases previas; no asumir versión por nombre. El manifiesto de cada sesión debe coincidir con el SHA final. visual_readings.json enlaza capturas finales con lectura directa o igualdad exacta de píxeles. No usar exit0 ni una carpeta existente como PASS. Dos últimas propiedades tienen lecturas en fused_HF16V3; inventario/estado en ui_HF16V3_*. JP sólo comparativo.

Reservas V3:G06:M100 depuración;G11:M011 frase de número de plantas. V2:G00:M252–255,G04:M033–034. Heredadas:G16:M073,preset32/F00:I053,consumidores G16:M000/M003/M004. La muestra getter no es un censo lingüístico completo. No hardware,segundo emulador,segundo revisor ni ruta natural universal.

Nueva región06:E588–06:F708 exclusivo,4480bytes; siguiente inicio posible06:F708 sólo tras verificar de nuevo. El inicio rechazado06:E586 contenía el terminador FFFF de G06:M099: nunca inferir espacio libre sólo por FF; comprobar extents heredados. Banco1B conserva ocupación QA20 hasta1B:EE88. G07 tabla066F40 y G16 tabla06CB86 tienen256 entradas fijas porque sus primeros recursos se relocalizaron.

F06:I019/I022 se corrigieron in situ. PROPERTY_UNDEAD_TEXT de la receta previa se fusionó conservando su preimagen original; QA21 edits registra la transición real HF15→HF16. Fuente compartida y código iguales. El codec es parcial: leer cada nuevo texto en el motor. Camilla's Dad conserva secuencia nativa especial. Professor se usa para先生 de Faukes en este lote; comprobar coherencia transversal enV5.

Checkpoints incluidos: evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss para diálogos y evidence/qa3/q3_dungeon/checkpoint.mss para inventario. Una instancia de Mesen a la vez. Límite de emergencia40min/turno; guardar checkpoint antes de cortar. Entrega siempre fuentes completas+BPS directoJP+evidencia sin ROM.
'''
(R/'PROJECT_CONTEXT.md').write_text(context);(R/'CONTEXTO_CONTINUACION.md').write_text(context)
p=R/'CHANGELOG.md';p.write_text('# QA21 / HF16 — Validación 3/5 (2026-10-15 UTC)\n\n207 referencias;64 diálogos y dos propiedades corregidos.205 aprobaciones sintéticas acotadas,dos reservas; inventario/estado y seis equipos fusionados comparados con JP.4258bytes vsHF15. Global abierto.\n\n'+p.read_text())
g=json.loads((R/'docs/quality_gates.json').read_text());g.update(version='HF16_TEST',audit_revision='QA21',qa21=v,qa21_supplemental=s,final_approved=False,global_linguistic_visual='V3_EXECUTED_SCOPED;V4_V5_AND_CONTEXTS_PENDING');(R/'docs/quality_gates.json').write_text(json.dumps(g,indent=2)+'\n')
notes=(Q/'notes_draft.txt').read_text()+'\nFinal:64 story edits plus2 getter property edits;4258changed bytes;SHA'+m['target']['sha256']+'. All final story sessions use verified_*; final consumer sessions ui_HF16V3_* and fused_HF16V3. Corrections of the obsolete test and allocator are documented, not hidden.\n';(Q/'NOTAS_QA21.md').write_text(notes)
for p in Q.iterdir():
 if p.is_file() and not p.name.startswith('library_'):shutil.copy2(p,R/'qa21'/p.name)
for sub in ['plans','supplemental_plans','fused_suite']:shutil.copytree(Q/sub,R/'qa21'/sub,dirs_exist_ok=True)
shutil.copytree(Q/'runs',R/'evidence/qa21_runs',dirs_exist_ok=True)
index=[]
for d in sorted((R/'evidence/qa21_runs').iterdir()):
 if (d/'run.json').exists():index.append({'run':d.name,'role':'FINAL_VERSION_EXECUTION'if d.name.startswith(('verified_','ui_HF16V3_','fused_HF16V3'))else'COMPARATIVE_OR_DIAGNOSTIC','metadata':json.loads((d/'run.json').read_text())})
(R/'docs/QA21_RUN_INDEX.json').write_text(json.dumps(index,indent=2)+'\n')
print({'references':v['references_reviewed'],'pass':v['scoped_pass'],'story_corrections':64,'getter_corrections':2,'native_final_sessions':207+s['final_native_sessions']})
