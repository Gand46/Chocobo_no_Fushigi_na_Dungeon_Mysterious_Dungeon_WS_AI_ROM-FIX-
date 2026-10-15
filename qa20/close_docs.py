from pathlib import Path
from datetime import datetime,timezone
import json,shutil,hashlib
R=Path('work/Chocobo_QA20_V2');Q=Path('qa20');v=json.loads((Q/'verification.json').read_text());m=json.loads((R/'manifest.json').read_text())
m['qa20']=v|{'unit_tests_passed':11,'portable_editable_rebuild':'PASS_EXACT_ROM_AND_EDITS','ui_context_pending':['G16:M000','G16:M003','G16:M004'],'second_independent_reviewer':False,'completed_utc':datetime.now(timezone.utc).isoformat()};m['generated_utc']=datetime.now(timezone.utc).isoformat();(R/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
text=f'''# Chocobo English v1.1 HF15 TEST — QA20, validación 2/5

V2 ejecutada con reservas: **248 referencias revisadas, 74 corregidas y 242 aprobaciones sintéticas acotadas**. Seis referencias necesitan su contexto. La aprobación visual/lingüística global sigue abierta; permanecen V3–V5.

## Resultado

- 248 selecciones de diálogo sobre HF15 final: 247 alcanzan el terminador. G00:M255 agota el límite y queda excluido del PASS.
- Cuatro sesiones adicionales de interfaz: inicio sin guardado, confirmación de carga con guardado, menú de guardar/escalera y carga en frío del guardado recién creado. 252 sesiones totales, {v['native_frames']} cuadros.
- {v['visual_readings']} capturas registradas: lectura directa o identidad exacta de píxeles con páginas leídas. Una sola revisión del asistente, sin segundo revisor independiente.
- {v['checks']} controles de integridad/alcance; 11 pruebas del proyecto aprobadas. 0 glifos no vacíos descartados en las 242 referencias aprobadas.
- Reconstrucción acumulativa, regeneración de las frases editables y aplicación independiente del BPS producen exactamente HF15.
- 4279 bytes distintos de HF14; 74 bloques y 74 punteros dentro del banco 1B. 4536 bytes de espacio previamente FF ocupados. Motor, gráficos, fuente, guardado y tamaño de ROM sin cambios.

## Qué se corrigió

Relaciones de causa y sujeto, omisiones de contenido, referencias a la maceta y al padre de Camilla, matices de preocupación/curiosidad, instrucciones de objetos y máquinas, y palabras incompletas. Se preserva la broma de las azadas antes de explicar la fusión de Talons. La paginación se adapta a dos líneas de 13 celdas usando los glifos nativos. El detalle de las 74 referencias está en qa20/translations.json y en QA20_V2_Informe.html.

## Reservas

G00:M252–255 requiere un contexto válido de depuración/variables. G00:M255 no termina en el estado forzado y descarta dos glifos no vacíos; no se aprueba. G04:M033–034 necesita ejecutar los consumidores de las preguntas y precios de forja. Leer sus recursos en la ventana común no demuestra ese uso.

Los menús reales de esta fase usan recursos getter; no se corresponden automáticamente con las etiquetas G16 de V1. Los consumidores propios G16:M000/M003/M004 permanecen pendientes de identificar/ejecutar. También permanecen G16:M073 (frase anfitriona) y preset32/F00:I053 (caller válido). No son seis reservas nuevas adicionales: las seis del lote se cuentan aparte de estos pendientes heredados/de interfaz.

No se valida recorrido natural completo, otro emulador ni hardware. Las causas históricas no reproducidas y el incidente eléctrico del cartucho conservan sus límites previos. Ver qa20/NOTAS_QA20.md para método y trazabilidad.

## Plan de cinco validaciones

| Validación | Referencias | Estado |
|---|---:|---|
| V1 | 83 | Ejecutada: 82 aprobaciones acotadas y G16:M073 pendiente. |
| V2 | 248 | Ejecutada: 242 aprobaciones acotadas y seis reservas. |
| V3 | 207 | Siguiente: resto de G06, G07, G08, G10, G11; objetos y variables. |
| V4 | 194 | Pendiente: G09 y diálogos extensos/opciones. |
| V5 | 154 | Pendiente: G14, transversal, gráficos/créditos y reservas. |

Las 886 referencias literales no abarcan por sí solas 2333 entradas getter, todos los consumidores ni gráficos. No se añade automáticamente otra validación ni se declara cierre global por el conteo.

## Uso y reconstrucción

Aplicar **Chocobo_EN_v1.1_HF15_TEST_JP_CCAA4853.bps** directamente sobre una copia limpia japonesa con CRC32 **CCAA4853**. El BPS es acumulativo; no se aplica sobre HF14 ni sobre una ROM inglesa.

```bash
python3 build.py '/ruta/Chocobo_JP.ws' --out '/ruta/salida_hf15'
python3 qa20/rebuild_translation_edits.py --japanese-rom '/ruta/Chocobo_JP.ws' --out '/ruta/frases_qa20'
python3 qa20/verify_scope.py --japanese-rom '/ruta/Chocobo_JP.ws' --out '/ruta/verificacion_qa20.json'
python3 -m unittest discover -s tests -v
```

El regenerador editable recompone HF14 desde las recetas incorporadas y aplica las frases QA20; no necesita recuperar un ZIP anterior. El builder canónico usa src/corrections.json. Cambiar translations.json requiere reintegrar los edits, no modifica automáticamente el BPS. Los scripts exploratorios con rutas de sesión se conservan como antecedentes, no son el camino portable de reconstrucción.

## Integridad

- ROM japonesa SHA-256: {m['original']['sha256']}
- ROM HF15 SHA-256: {m['target']['sha256']}
- CRC32 HF15: {m['target']['crc32']}; checksum WS: {m['target']['ws_checksum']}.
- BPS SHA-256: {m['bps_sha256']}

Fuentes acumulativas editables reconstruidas, evidencia e historial preservados; no son el código fuente original del juego. No se distribuyen ROM comercial, BIOS ni emulador. HF14 pasa a patches/historical con su hash intacto y migración registrada. Los controles históricos QA19 pasan sobre su HF14 preservado; no se presentan como ejecución nueva de V1 sobre HF15.

Los resultados de dos reconstrucciones desde extracciones nuevas del ZIP se registran en .continuity/reports. La receta conserva BPS e informe de compilación, sin incorporar la ROM generada como artefacto del paquete.
'''
(R/'README.md').write_text(text);(R/'INFORME_ES.md').write_text(text)
context='''# Continuación — autoridad HF15 / QA20 V2

Objetivo vigente: aprobación visual/lingüística global en cinco validaciones. V2 ejecutada con 248 lecturas bilingües, 74 referencias corregidas, 242 PASS sintéticos acotados y seis reservas. Global sigue abierto. Siguiente trabajo: V3, 207 referencias de la partición qa19/five_validation_plan.json. No repetir toda V1/V2 indiscriminadamente.

Partir de estas fuentes acumulativas HF15; validar .continuity antes de editar. build.py reconstruye desde JP CCAA4853. qa20/rebuild_translation_edits.py regenera las frases desde las recetas previas incorporadas. Leer README.md y qa20/NOTAS_QA20.md. La ROM final es 2189490744c44fb1f16f79216a4c861cb7e3ade185a86e4d05b556c1bf46dd43.

Reservas V2: G00:M252–255 (depuración/variables sin contexto coherente; M255 no termina en 2400 cuadros), G04:M033–034 (consumidores de forja). De V1/UI: G16:M000/M003/M004 aún no vinculados a consumidores propios; los menús probados usan getters, no esas etiquetas. G16:M073 requiere frase anfitriona; preset32/F00:I053 sigue sin caller válido. No inferir consumidor por texto parecido ni recurso sin uso por ausencia de una firma de script.

248 sesiones de diálogo sobre HF15: 247 terminadores alcanzados y un diagnóstico excluido. Cuatro sesiones UI adicionales; 252 en total. Sólo las 242 aprobadas están libres de descartes no vacíos y tienen lectura lingüística acotada. No usar exit=0 como PASS. Las imágenes finales son idénticas a lecturas directas previas o se leyeron directamente; visual_readings.json registra la procedencia. No hay segundo revisor.

Se ocupó 1B:DCD0–1B:EE87, 4536 bytes de área FF verificada. Nuevo fin libre 1B:EE88; verificar otra vez antes de futuras escrituras. 74 punteros del mismo banco modificados; no se cambió código o fuente. El generador del codec sigue siendo parcial; cada frase nueva exige lectura nativa, especialmente medias celdas. «Camilla's Dad» usa una secuencia ya existente; no es «Camilla and her dad».

Checkpoints: diálogo evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss; guardado evidence/qa13_runs/q13_equipment_checkpoint/fullbag_checked_checkpoint.mss. Planes exactos en evidence/qa20_runs/release_*/plan.lua. Una instancia de Mesen a la vez. Reanudar desde evidencia release_*, no desde el nombre engañoso final_* de una tanda diagnóstica.

V3 conserva sus 207 referencias; V4 194, V5 154 más transversal/reservas. No añadir automáticamente una sexta fase ni declarar aprobación universal. Los PASS sintéticos autorizados no prueban hardware o ruta natural. Mantener entrega de fuentes completas acumulativas + BPS directo JP + evidencia, sin ROM. Límite de emergencia: 40 minutos por turno; preservar checkpoint antes de cortar.
'''
(R/'PROJECT_CONTEXT.md').write_text(context);(R/'CONTEXTO_CONTINUACION.md').write_text(context)
p=R/'CHANGELOG.md';p.write_text('# QA20 / HF15 — Visual y lingüística V2 (2026-10-14)\n\n248 referencias revisadas, 74 corregidas; 242 aprobaciones sintéticas acotadas y seis reservas. 4279 bytes frente a HF14. Fuentes completas y BPS acumulativo directo JP. Sin aprobación global.\n\n'+p.read_text())
g=json.loads((R/'docs/quality_gates.json').read_text());g['historical_version_label']=g['version'];g['version']='HF15_TEST';g['audit_revision']='QA20';g['qa20']=v;g['final_approved']=False;g['global_linguistic_visual']='V2_EXECUTED_SCOPED;V3_V4_V5_AND_CONTEXTS_PENDING';(R/'docs/quality_gates.json').write_text(json.dumps(g,indent=2)+'\n')
for p in Q.iterdir():
 if p.is_file():shutil.copy2(p,R/'qa20'/p.name)
index=[]
for d in sorted((R/'evidence/qa20_runs').iterdir()):
 if (d/'run.json').exists():index.append({'run':d.name,'role':'FINAL_VERSION_EXECUTION'if d.name.startswith('release_')else'DIAGNOSTIC_OR_DIRECT_READING','metadata':json.loads((d/'run.json').read_text())})
(R/'docs/QA20_RUN_INDEX.json').write_text(json.dumps(index,indent=2)+'\n')
print({'source_root':str(R),'checks':v['checks'],'final_native_sessions':v['native_sessions_final']})
